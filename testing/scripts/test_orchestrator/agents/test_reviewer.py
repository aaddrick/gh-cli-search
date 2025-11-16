"""Test reviewer agent invocation"""

import subprocess
from pathlib import Path
from typing import List

from ..config import TEST_REVIEWER_AGENT, REPO_ROOT


def run_test_reviewer(report_dir: Path, all_report_dirs: List[Path], start_commit_id: str, verbose: bool = False) -> bool:
    """Invoke the test-reviewer agent as a headless agent

    Args:
        report_dir: Current test run report directory
        all_report_dirs: List of all report directories (existing + current)
        start_commit_id: Git commit ID when test run started
        verbose: Whether to show real-time agent output

    Returns:
        True if reviewer completed successfully
    """
    print("\n" + "=" * 60)
    print("RUNNING TEST REVIEWER AGENT")
    print("=" * 60)
    print(f"Analyzing results in: {report_dir}")
    if verbose:
        print("(Verbose mode: real-time agent output)")
    print()

    # Determine which run this is in the current session
    run_number = len(all_report_dirs)

    # Check for previous run's PM-NOTES for context
    previous_pm_notes = None
    if run_number > 1:
        # Previous run is the one before current in the list
        prev_dir = all_report_dirs[-2]  # -2 because -1 is current, -2 is previous
        pm_notes_path = prev_dir / "PM-NOTES.md"
        if pm_notes_path.exists():
            previous_pm_notes = str(pm_notes_path)
            print(f"Found previous PM-NOTES for context: {prev_dir.name}/PM-NOTES.md")

    # Read the agent definition
    agent_prompt = TEST_REVIEWER_AGENT.read_text()

    # Add previous PM-NOTES context if available
    pm_context = ""
    if previous_pm_notes:
        pm_context = f"""
PREVIOUS PRODUCT MANAGER CONTEXT:
The previous iteration's product manager analysis is available at: {previous_pm_notes}

READ THIS FIRST to understand:
- What the PM identified as key issues
- What was expected to improve
- What direction the PM thinks testing should head
- PM's concerns from the previous iteration

This helps you focus your analysis and see if you're heading in the right direction.
"""

    # Create the full prompt for the agent
    full_prompt = f"""You are executing as a headless test-reviewer agent.

Your task is to analyze the test suite results and create REVIEWER-NOTES.md.

The test results are located in: {report_dir}
Git commit ID when test started: {start_commit_id}
{pm_context}
Follow these instructions from the agent definition:

{agent_prompt}

IMPORTANT:
1. **FIRST**: Read testing/GUIDANCE.md for human decisions and product philosophy
2. Use the report directory: {report_dir}
3. {"Check for and read previous PM-NOTES if it exists (path provided above)" if previous_pm_notes else "This is the first test run in this session (no previous PM context)"}
4. Write REVIEWER-NOTES.md to: {report_dir}/REVIEWER-NOTES.md
5. **CRITICAL**: Start REVIEWER-NOTES.md with a header line: "**Git Commit:** {start_commit_id}" before any other content
6. Be thorough but efficient - sample 3-5 representative failures
7. Question test validity before assuming skills are wrong (per GUIDANCE.md)
8. Provide specific, actionable recommendations that respect GUIDANCE.md

Begin your analysis now."""

    try:
        # Execute headless agent
        # In verbose mode, output goes directly to terminal; otherwise capture it
        result = subprocess.run(
            [
                'claude',
                '-p', full_prompt,
                '--output-format', 'text',
                '--allowedTools', 'Read,Bash,Write,Grep',
                '--permission-mode', 'bypassPermissions'
            ],
            capture_output=not verbose,
            text=True,
            timeout=300,  # 5 minute timeout
            cwd=str(REPO_ROOT)
        )

        if result.returncode == 0:
            print("✓ Test reviewer completed successfully")
            print(f"\nReviewer notes: {report_dir}/REVIEWER-NOTES.md")
            return True
        else:
            print(f"✗ Test reviewer failed with exit code {result.returncode}")
            if not verbose and result.stderr:
                print(f"Error: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("✗ Test reviewer timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"✗ Test reviewer error: {str(e)}")
        return False
