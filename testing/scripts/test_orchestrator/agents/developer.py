"""Developer agent invocation"""

import subprocess
from pathlib import Path

from ..config import DEVELOPER_AGENT, REPO_ROOT


def run_developer_agent(report_dir: Path, verbose: bool = False) -> bool:
    """Invoke the developer agent to implement fixes from reviewer/PM recommendations

    Args:
        report_dir: Current test run report directory
        verbose: Whether to show real-time agent output

    Returns:
        True if developer completed successfully
    """
    print("\n" + "=" * 60)
    print("RUNNING DEVELOPER AGENT")
    print("=" * 60)
    print(f"Implementing fixes for: {report_dir.name}")
    print(f"Working directory: {report_dir}")
    if verbose:
        print("(Verbose mode: real-time agent output)")
    print()

    # Check for required input files
    reviewer_notes = report_dir / "REVIEWER-NOTES.md"
    pm_notes = report_dir / "PM-NOTES.md"

    if not reviewer_notes.exists():
        print(f"⚠️  Warning: {reviewer_notes.name} not found")
    else:
        print(f"✓ Found {reviewer_notes.name}")

    if not pm_notes.exists():
        print(f"⚠️  Warning: {pm_notes.name} not found")
    else:
        print(f"✓ Found {pm_notes.name}")

    print()

    # Read the agent definition
    agent_prompt = DEVELOPER_AGENT.read_text()

    # Create the full prompt for the agent
    full_prompt = f"""You are executing as a headless developer agent.

Your task is to implement the recommendations from the test-reviewer and product-manager to fix test failures.

The test results and recommendations are located in: {report_dir}

Available files:
- REPORT.md: Test results with full failure details
- REVIEWER-NOTES.md: Test reviewer's analysis and recommendations
- PM-NOTES.md: Product manager's decision and priorities

Follow these instructions from the agent definition:

{agent_prompt}

IMPORTANT:
1. **FIRST**: Read testing/GUIDANCE.md for human decisions and product philosophy
2. Read PM-NOTES.md to understand priorities (HIGH/MEDIUM/LOW)
3. Read REVIEWER-NOTES.md for detailed failure analysis
4. Implement high-priority fixes that align with GUIDANCE.md philosophy
5. Validate your changes (syntax, format, etc.)
6. Write DEVELOPER-NOTES.md to: {report_dir}/DEVELOPER-NOTES.md
7. Document every change with rationale
8. Be conservative - make targeted fixes only
9. Set realistic expectations for next test run

You have 10 minutes. Focus on high-impact changes first.
Remember: GUIDANCE.md contains critical decisions about when to fix tests vs skills.

Begin your implementation now."""

    try:
        # Execute headless agent
        # In verbose mode, output goes directly to terminal; otherwise capture it
        result = subprocess.run(
            [
                'claude',
                '-p', full_prompt,
                '--output-format', 'text',
                '--allowedTools', 'Read,Write,Edit,Bash,Grep,Glob',
                '--permission-mode', 'bypassPermissions'
            ],
            capture_output=not verbose,
            text=True,
            timeout=600,  # 10 minute timeout
            cwd=str(REPO_ROOT)
        )

        if result.returncode == 0:
            print("✓ Developer agent completed successfully")

            # Check if DEVELOPER-NOTES.md was created
            dev_notes = report_dir / "DEVELOPER-NOTES.md"
            if dev_notes.exists():
                print(f"✓ Created {dev_notes.name}")
                print(f"\nDeveloper notes: {report_dir}/DEVELOPER-NOTES.md")
                return True
            else:
                print(f"⚠️  Warning: Developer agent completed but {dev_notes.name} was not created")
                print("This may indicate the agent didn't make any changes")
                return True  # Still return True - agent ran successfully even if no changes needed
        else:
            print(f"✗ Developer agent failed with exit code {result.returncode}")
            if not verbose and result.stderr:
                print(f"Error: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("✗ Developer agent timed out after 10 minutes")
        return False
    except Exception as e:
        print(f"✗ Developer agent error: {str(e)}")
        return False
