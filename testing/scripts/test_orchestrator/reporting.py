"""Test result reporting and output generation"""

from pathlib import Path
from datetime import datetime
from typing import List, Dict

from .models import TestResult


def write_test_report(report_dir: Path, test_result: TestResult) -> None:
    """Write individual test report

    Args:
        report_dir: Directory to write report to
        test_result: Test result data
    """
    report_path = report_dir / f"{test_result.test_num}.md"

    with open(report_path, 'w') as f:
        f.write(f"# Test {test_result.test_num}: {test_result.test_name}\n\n")
        f.write(f"**Status:** {test_result.status}\n\n")
        f.write(f"**Duration:** {test_result.duration_seconds:.2f}s\n\n")
        f.write(f"**User Request:** \"{test_result.user_request}\"\n\n")
        f.write(f"**Command Generated:**\n```bash\n{test_result.command_generated}\n```\n\n")

        f.write(f"**Expected Criteria:**\n")
        for criterion in test_result.criteria:
            f.write(f"- {criterion}\n")
        f.write("\n")

        if test_result.status == "FAIL":
            f.write(f"**Failure Reason:**\n{test_result.failure_reason}\n\n")

        f.write(f"**Full Output:**\n```\n{test_result.output[:2000]}{'...' if len(test_result.output) > 2000 else ''}\n```\n")


def write_group_report(report_dir: Path, group_name: str, results: List[TestResult]) -> None:
    """Write group report for a scenario file

    Args:
        report_dir: Directory to write report to
        group_name: Name of the test group
        results: List of test results for this group
    """
    report_path = report_dir / "REPORT.md"

    passed = sum(1 for r in results if r.status == "PASS" or r.status == "SKIPPED")
    failed = sum(1 for r in results if r.status == "FAIL")
    total = len(results)
    pass_rate = (passed / total * 100) if total > 0 else 0

    # Calculate timing statistics
    total_duration = sum(r.duration_seconds for r in results)
    avg_duration = total_duration / total if total > 0 else 0
    min_duration = min(r.duration_seconds for r in results) if results else 0
    max_duration = max(r.duration_seconds for r in results) if results else 0

    with open(report_path, 'w') as f:
        f.write(f"# Test Group Report: {group_name}\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Group Name:** {group_name}\n\n")

        f.write(f"## Summary\n\n")
        f.write(f"- **Total Tests:** {total}\n")
        f.write(f"- **Passed:** {passed} ({pass_rate:.1f}%)\n")
        f.write(f"- **Failed:** {failed}\n")
        f.write(f"- **Total Duration:** {total_duration:.1f}s ({total_duration/60:.1f}m)\n")
        f.write(f"- **Average Duration:** {avg_duration:.1f}s per test\n")
        f.write(f"- **Duration Range:** {min_duration:.1f}s - {max_duration:.1f}s\n\n")

        f.write(f"## Test Results\n\n")
        for result in results:
            status_icon = "✓" if result.status in ["PASS", "SKIPPED"] else "✗"
            f.write(f"### Test {result.test_num}: {result.test_name}\n")
            f.write(f"- **Status:** {status_icon} {result.status}\n")
            f.write(f"- **Duration:** {result.duration_seconds:.1f}s\n")
            f.write(f"- **User Request:** \"{result.user_request}\"\n")
            f.write(f"- **Command Generated:** `{result.command_generated}`\n")
            if result.status == "FAIL":
                f.write(f"- **Issue:** {result.failure_reason}\n")
            f.write(f"- **Report:** [./{result.test_num}.md](./{result.test_num}.md)\n\n")


def write_master_report(report_dir: Path, all_results: Dict[str, List[TestResult]]) -> None:
    """Write master consolidated report

    Args:
        report_dir: Directory to write report to
        all_results: Dictionary mapping group names to test results
    """
    report_path = report_dir / "REPORT.md"

    total_tests = sum(len(results) for results in all_results.values())
    total_passed = sum(sum(1 for r in results if r.status in ["PASS", "SKIPPED"]) for results in all_results.values())
    total_failed = sum(sum(1 for r in results if r.status == "FAIL") for results in all_results.values())
    pass_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0

    # Calculate timing statistics
    all_test_results = [r for results in all_results.values() for r in results]
    total_duration = sum(r.duration_seconds for r in all_test_results)
    avg_duration = total_duration / total_tests if total_tests > 0 else 0
    min_duration = min(r.duration_seconds for r in all_test_results) if all_test_results else 0
    max_duration = max(r.duration_seconds for r in all_test_results) if all_test_results else 0

    with open(report_path, 'w') as f:
        f.write(f"# GH CLI Search Skills - Test Suite Report\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Report:** {report_dir.name.split('_')[-1]}\n\n")

        f.write(f"## Summary\n\n")
        f.write(f"- **Total Test Groups:** {len(all_results)}\n")
        f.write(f"- **Total Tests:** {total_tests}\n")
        f.write(f"- **Passed:** {total_passed} ({pass_rate:.1f}%)\n")
        f.write(f"- **Failed:** {total_failed} ({100-pass_rate:.1f}%)\n")
        f.write(f"- **Total Duration:** {total_duration:.1f}s ({total_duration/60:.1f}m)\n")
        f.write(f"- **Average Duration:** {avg_duration:.1f}s per test\n")
        f.write(f"- **Duration Range:** {min_duration:.1f}s - {max_duration:.1f}s\n\n")

        f.write(f"## Results by Group\n\n")
        for group_name, results in sorted(all_results.items()):
            total = len(results)
            passed = sum(1 for r in results if r.status in ["PASS", "SKIPPED"])
            failed = sum(1 for r in results if r.status == "FAIL")
            group_rate = (passed / total * 100) if total > 0 else 0

            f.write(f"### {group_name}\n")
            f.write(f"- **Tests:** {total}\n")
            f.write(f"- **Passed:** {passed}\n")
            f.write(f"- **Failed:** {failed}\n")
            f.write(f"- **Pass Rate:** {group_rate:.1f}%\n")
            f.write(f"- **Report:** [./{group_name}/REPORT.md](./{group_name}/REPORT.md)\n\n")

        # Failed tests summary
        f.write(f"## Failed Tests Summary\n\n")
        has_failures = False
        for group_name, results in sorted(all_results.items()):
            failed_tests = [r for r in results if r.status == "FAIL"]
            if failed_tests:
                has_failures = True
                f.write(f"### {group_name}\n\n")
                for result in failed_tests:
                    f.write(f"**Test {result.test_num}: {result.test_name}**\n\n")
                    f.write(f"**Status:** {result.status}\n\n")
                    f.write(f"**Duration:** {result.duration_seconds:.1f}s\n\n")
                    f.write(f"**User Request:** \"{result.user_request}\"\n\n")
                    f.write(f"**Command Generated:**\n```bash\n{result.command_generated}\n```\n\n")
                    f.write(f"**Expected Criteria:**\n")
                    for criterion in result.criteria:
                        f.write(f"- {criterion}\n")
                    f.write("\n")
                    f.write(f"**Failure Reason:**\n{result.failure_reason}\n\n")
                    f.write(f"**Full Output:**\n```\n{result.output[:2000]}{'...' if len(result.output) > 2000 else ''}\n```\n\n")
                    f.write(f"**Full Report:** [./{group_name}/{result.test_num}.md](./{group_name}/{result.test_num}.md)\n\n")
                    f.write("---\n\n")

        if not has_failures:
            f.write("No test failures - all tests passed!\n\n")

        f.write(f"## Test Execution Details\n\n")
        f.write(f"- **Scenario Files Processed:** {len(all_results)}\n")
        f.write(f"- **Tests Executed:** {total_tests}\n")
