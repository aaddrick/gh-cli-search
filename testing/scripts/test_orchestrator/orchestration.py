"""Test orchestration and main execution loop"""

import re
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed

from .config import REPO_ROOT, SCENARIOS_DIR, REPORTS_BASE, MAX_TEST_ITERATIONS
from .models import TestResult
from .scenarios import parse_scenario_file
from .execution import process_single_test
from .reporting import write_group_report, write_master_report
from .agents import run_test_reviewer, run_product_manager, run_developer_agent


def get_current_commit_id() -> str:
    """Get the current git commit ID

    Returns:
        Commit ID (short hash) or 'unknown' if unable to determine
    """
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--short', 'HEAD'],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return 'unknown'


def scan_existing_report_dirs() -> List[Path]:
    """Scan REPORTS_BASE for existing report directories and return sorted list

    Returns:
        List of Path objects for existing report directories, sorted chronologically
    """
    if not REPORTS_BASE.exists():
        return []

    # Pattern: yyyy-mm-dd_N
    pattern = re.compile(r'^(\d{4}-\d{2}-\d{2})_(\d+)$')

    report_dirs = []
    for entry in REPORTS_BASE.iterdir():
        if entry.is_dir():
            match = pattern.match(entry.name)
            if match:
                date_str = match.group(1)
                sequence = int(match.group(2))
                report_dirs.append((date_str, sequence, entry))

    # Sort by date first, then by sequence number
    report_dirs.sort(key=lambda x: (x[0], x[1]))

    # Return just the Path objects
    return [entry for _, _, entry in report_dirs]


def run_test_suite(report_dir: Path, workers: int) -> Dict[str, List[TestResult]]:
    """Execute the test suite and return results

    Args:
        report_dir: Directory to write reports to
        workers: Number of parallel worker threads

    Returns:
        Dictionary mapping group names to lists of test results
    """
    # Get all scenario files
    scenario_files = sorted(SCENARIOS_DIR.glob("*-tests.md"))
    all_results = {}

    for scenario_file in scenario_files:
        group_name = scenario_file.stem  # e.g., 'gh-search-code-tests'
        print(f"Processing {group_name}...")

        # Parse tests
        tests = parse_scenario_file(scenario_file)
        print(f"  Found {len(tests)} tests")

        # Create group directory
        group_dir = report_dir / group_name
        group_dir.mkdir(exist_ok=True)

        # Execute tests in parallel
        results = []
        with ThreadPoolExecutor(max_workers=workers) as executor:
            # Submit all tests
            future_to_test = {
                executor.submit(process_single_test, test, group_name, group_dir): test
                for test in tests
            }

            # Collect results as they complete
            for future in as_completed(future_to_test):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    test = future_to_test[future]
                    print(f"  Test {test['test_num']} raised exception: {e}")

        # Sort results by test number for consistent ordering
        results.sort(key=lambda r: r.test_num)

        # Write group report
        write_group_report(group_dir, group_name, results)
        all_results[group_name] = results

        passed = sum(1 for r in results if r.status in ["PASS", "SKIPPED"])
        print(f"  Group complete: {passed}/{len(results)} passed\n")

    # Write master report
    write_master_report(report_dir, all_results)

    return all_results


def main():
    """Main execution with iteration loop"""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Run gh-cli-search test suite with parallel execution and automated review'
    )
    parser.add_argument(
        '--workers',
        type=int,
        default=8,
        help='Number of parallel test workers (default: 8)'
    )
    parser.add_argument(
        '--no-review',
        action='store_true',
        help='Skip automatic test-reviewer and product-manager agent execution'
    )
    parser.add_argument(
        '--no-pm',
        action='store_true',
        help='Skip product-manager decision (run review but halt after)'
    )
    parser.add_argument(
        '--no-dev',
        action='store_true',
        help='Skip developer agent (PM decides rerun but no fixes implemented)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show real-time agent output instead of capturing it'
    )
    args = parser.parse_args()

    overall_start_time = datetime.now()
    start_commit_id = get_current_commit_id()

    print("GH CLI Search Skills - Test Suite Execution")
    print("=" * 60)
    print(f"Start time: {overall_start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Git commit: {start_commit_id}")
    print(f"Parallel workers: {args.workers}")
    print(f"Automated review: {'Disabled' if args.no_review else 'Enabled'}")
    print(f"Product manager: {'Disabled' if args.no_review or args.no_pm else 'Enabled'}")
    print(f"Developer agent: {'Disabled' if args.no_review or args.no_pm or args.no_dev else 'Enabled'}")
    print(f"Verbose mode: {'Enabled' if args.verbose else 'Disabled'}")
    print()

    # Scan for existing report directories (from all previous script runs)
    all_report_dirs = scan_existing_report_dirs()
    if all_report_dirs:
        print(f"Found {len(all_report_dirs)} existing report director{'y' if len(all_report_dirs) == 1 else 'ies'}:")
        for report_dir in all_report_dirs:
            print(f"  - {report_dir.name}")
        print()

    # Track all report directories (existing + new ones created in this run)
    date_str = overall_start_time.strftime('%Y-%m-%d')

    iteration = 1
    should_continue = True

    while should_continue and iteration <= MAX_TEST_ITERATIONS:
        print("\n" + "=" * 60)
        print(f"TEST RUN {iteration}/{MAX_TEST_ITERATIONS}")
        print("=" * 60)

        iteration_start_time = datetime.now()

        # Find next available report directory number
        count = 1
        while (REPORTS_BASE / f"{date_str}_{count}").exists():
            count += 1
        report_dir = REPORTS_BASE / f"{date_str}_{count}"
        all_report_dirs.append(report_dir)

        report_dir.mkdir(parents=True, exist_ok=True)
        print(f"Report directory: {report_dir}\n")

        # Run test suite
        all_results = run_test_suite(report_dir, args.workers)

        # Calculate summary statistics
        iteration_end_time = datetime.now()
        duration = iteration_end_time - iteration_start_time
        total_tests = sum(len(results) for results in all_results.values())
        total_passed = sum(sum(1 for r in results if r.status in ["PASS", "SKIPPED"]) for results in all_results.values())
        total_failed = total_tests - total_passed
        pass_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0

        # Print test run summary
        print()
        print("=" * 60)
        print(f"TEST RUN {iteration} COMPLETE")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {total_passed} ({pass_rate:.1f}%)")
        print(f"Failed: {total_failed}")
        print(f"\nExecution Time: {duration.total_seconds():.1f} seconds ({duration.total_seconds()/60:.1f} minutes)")
        print(f"Average: {duration.total_seconds()/total_tests:.1f} seconds per test")
        print(f"\nReport location: {report_dir}/REPORT.md")

        # Run review and decision process unless disabled
        if args.no_review:
            print("\nSkipping review and PM (--no-review flag set)")
            should_continue = False
        else:
            # Run test reviewer
            reviewer_success = run_test_reviewer(report_dir, all_report_dirs, start_commit_id, args.verbose)

            if not reviewer_success:
                print("\n⚠️  Test reviewer failed, halting test run loop")
                should_continue = False
            elif args.no_pm:
                print("\nSkipping product manager (--no-pm flag set)")
                should_continue = False
            else:
                # Run product manager to decide next step
                pm_decision = run_product_manager(report_dir, all_report_dirs, start_commit_id, MAX_TEST_ITERATIONS, args.verbose)

                action = pm_decision.get('action', 'halt')

                if action == 'rerun' and iteration < MAX_TEST_ITERATIONS:
                    print(f"\n🔄 Product manager decided to RE-RUN tests (next run will be {iteration + 1}/{MAX_TEST_ITERATIONS})")
                    print(f"Reasoning: {pm_decision.get('reasoning', 'No reasoning provided')}")

                    # Run developer agent to implement fixes before next test run (unless --no-dev)
                    if args.no_dev:
                        print("\nSkipping developer agent (--no-dev flag set)")
                        print("⚠️  WARNING: Re-running tests without implementing fixes!")
                        iteration += 1
                        should_continue = True
                    else:
                        developer_success = run_developer_agent(report_dir, args.verbose)

                        if not developer_success:
                            print("\n⚠️  Developer agent failed, halting test run loop")
                            print("Human intervention may be needed to implement fixes")
                            should_continue = False
                        else:
                            print(f"\n✓ Developer agent completed, proceeding to test run {iteration + 1}")
                            iteration += 1
                            should_continue = True
                elif action == 'rerun' and iteration >= MAX_TEST_ITERATIONS:
                    print(f"\n⚠️  Product manager wanted to re-run, but maximum test runs ({MAX_TEST_ITERATIONS}) reached")
                    print("Halting for human feedback")
                    should_continue = False
                else:  # halt
                    print("\n✋ Product manager decided to HALT for human feedback")
                    print(f"Reasoning: {pm_decision.get('reasoning', 'No reasoning provided')}")

                    if 'human_tasks' in pm_decision and pm_decision['human_tasks']:
                        print("\nHuman tasks needed:")
                        for task in pm_decision['human_tasks']:
                            print(f"  • {task}")

                    should_continue = False

    # Final summary
    overall_end_time = datetime.now()
    overall_duration = overall_end_time - overall_start_time

    print("\n" + "=" * 60)
    print("TEST EXECUTION COMPLETE")
    print("=" * 60)
    print(f"Total test runs: {iteration}")
    print(f"Total execution time: {overall_duration.total_seconds():.1f} seconds ({overall_duration.total_seconds()/60:.1f} minutes)")

    if iteration == 1:
        print(f"\nFinal report: {all_report_dirs[0]}/REPORT.md")
    else:
        print(f"\nAll test run reports in: {REPORTS_BASE}/")
        for i, report_dir in enumerate(all_report_dirs, 1):
            print(f"  - Test run {i}: {report_dir.name}/")
