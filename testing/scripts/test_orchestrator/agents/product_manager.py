"""Product manager agent invocation"""

import subprocess
import json
import re
from pathlib import Path
from typing import List, Dict

from ..config import PRODUCT_MANAGER_AGENT, REPO_ROOT


def run_product_manager(report_dir: Path, all_report_dirs: List[Path], start_commit_id: str, max_runs: int, verbose: bool = False) -> Dict:
    """Invoke the product-manager agent as a headless agent to make re-run decision

    Args:
        report_dir: Current test run report directory
        all_report_dirs: List of all report directories (existing + current)
        start_commit_id: Git commit ID when test run started
        max_runs: Maximum number of test runs allowed
        verbose: Whether to show real-time agent output

    Returns:
        Dictionary with decision: {"action": "rerun"|"halt", "reasoning": str, "confidence": str}
    """
    print("\n" + "=" * 60)
    print("RUNNING PRODUCT MANAGER AGENT")
    print("=" * 60)
    print(f"Reviewing results in: {report_dir}")

    # Determine which run this is in the current session
    run_number = len(all_report_dirs)
    print(f"Current test run: {run_number}/{max_runs}")
    if verbose:
        print("(Verbose mode: real-time agent output)")

    # Build previous run directories list
    previous_runs = []
    if run_number > 1:
        # All previous runs from the list (everything before current)
        for prev_dir in all_report_dirs[:-1]:  # All except the last (current)
            if (prev_dir / "PM-NOTES.md").exists():
                previous_runs.append(str(prev_dir))

    # Display previous runs info
    if run_number > 1:
        print(f"\nChecking {len(previous_runs)} previous test run(s) for context:")
        for i, prev_dir in enumerate(previous_runs, 1):
            print(f"  - Run {i}: {Path(prev_dir).name}")
    else:
        print("\nFirst test run in this session (no previous context)")

    print()

    # Read the agent definition
    agent_prompt = PRODUCT_MANAGER_AGENT.read_text()

    # Build previous runs context
    prev_context = ""
    if previous_runs:
        prev_context = f"""
PREVIOUS TEST RUNS IN THIS SESSION:
This is test run {run_number} of this script execution. Previous runs exist. You MUST review previous PM-NOTES.md files:
"""
        for i, prev_dir in enumerate(previous_runs, 1):
            prev_context += f"- Run {i}: {prev_dir}/PM-NOTES.md\n"

        prev_context += """
CRITICAL: Read these previous PM-NOTES to understand:
- What was expected to improve
- What actually improved
- Decision trajectory and reasoning
- Whether we're seeing diminishing returns

Use this context to make an informed decision about continuing or halting.
"""

    # Create the full prompt for the agent
    full_prompt = f"""You are executing as a headless product-manager agent.

Your task is to review the test results and decide whether to re-run tests or halt for human feedback.

The test results are located in: {report_dir}
Git commit ID when test started: {start_commit_id}
Current test run: {run_number} of {max_runs} allowed in this script execution
{prev_context}
Follow these instructions from the agent definition:

{agent_prompt}

IMPORTANT:
1. **FIRST**: Read testing/GUIDANCE.md for human decisions and product philosophy
2. Use the report directory: {report_dir}
3. Read REPORT.md for test results
4. Read REVIEWER-NOTES.md for failure analysis
5. {"**READ PREVIOUS PM-NOTES.md FILES** (listed above)" if previous_runs else "This is the first test run in this session (no previous context)"}
6. Write PM-NOTES.md to: {report_dir}/PM-NOTES.md
7. **CRITICAL**: Start PM-NOTES.md with a header line: "**Git Commit:** {start_commit_id}" before any other content
8. Output valid JSON with your decision (must respect GUIDANCE.md decisions)
9. Consider run count - after {max_runs} test runs, the script will halt

Your JSON output will be parsed by the Python script to determine next steps.

Begin your analysis now."""

    try:
        # Execute headless agent with JSON output
        # Note: PM always captures output because we need to parse JSON decision
        # In verbose mode, we just log that we're waiting for PM decision
        if verbose:
            print("Note: PM output is captured (not streamed) to parse JSON decision\n")

        result = subprocess.run(
            [
                'claude',
                '-p', full_prompt,
                '--output-format', 'json',
                '--allowedTools', 'Read,Bash,Write,Grep',
                '--permission-mode', 'bypassPermissions'
            ],
            capture_output=True,  # Always capture for PM to parse JSON
            text=True,
            timeout=180,  # 3 minute timeout
            cwd=str(REPO_ROOT)
        )

        if result.returncode != 0:
            print(f"✗ Product manager failed with exit code {result.returncode}")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return {"action": "halt", "reasoning": "Product manager execution failed", "confidence": "low"}

        # Parse JSON output
        try:
            output_data = json.loads(result.stdout)

            # Extract the result from the JSON response
            # The output format includes metadata, so we need to get the actual result
            if 'result' in output_data:
                result_text = output_data['result']
                # Try to find JSON in the result text
                # Look for JSON object pattern
                json_match = re.search(r'\{[^{}]*"action"[^{}]*\}', result_text, re.DOTALL)
                if json_match:
                    decision = json.loads(json_match.group(0))
                else:
                    # Fallback: try parsing the entire result as JSON
                    decision = json.loads(result_text)
            else:
                # Direct JSON output
                decision = output_data

            # Validate decision structure
            if 'action' not in decision or decision['action'] not in ['rerun', 'halt']:
                print(f"✗ Invalid decision format: {decision}")
                return {"action": "halt", "reasoning": "Invalid decision format from PM", "confidence": "low"}

            # Display decision
            action = decision['action']
            reasoning = decision.get('reasoning', 'No reasoning provided')
            confidence = decision.get('confidence', 'unknown')

            print(f"✓ Product manager completed successfully")
            print(f"\nDecision: {action.upper()}")
            print(f"Confidence: {confidence}")
            print(f"Reasoning: {reasoning}")
            print(f"\nPM notes: {report_dir}/PM-NOTES.md")

            return decision

        except json.JSONDecodeError as e:
            print(f"✗ Failed to parse product manager JSON output: {e}")
            print(f"Output was: {result.stdout[:500]}")
            return {"action": "halt", "reasoning": "Failed to parse PM decision JSON", "confidence": "low"}

    except subprocess.TimeoutExpired:
        print("✗ Product manager timed out after 3 minutes")
        return {"action": "halt", "reasoning": "Product manager timeout", "confidence": "low"}
    except Exception as e:
        print(f"✗ Product manager error: {str(e)}")
        return {"action": "halt", "reasoning": f"Product manager exception: {str(e)}", "confidence": "low"}
