"""Test execution and processing"""

import subprocess
from pathlib import Path
from datetime import datetime
from typing import Tuple, Dict

from .config import RUN_TEST_SCRIPT, print_lock
from .models import TestResult
from .validation import extract_command, validate_test
from .reporting import write_test_report


def run_single_test(user_request: str) -> Tuple[str, str]:
    """Execute a single test using run-single-test.sh

    Args:
        user_request: The user's test request string

    Returns:
        Tuple of (stdout, stderr)
    """
    try:
        result = subprocess.run(
            [str(RUN_TEST_SCRIPT), user_request],
            capture_output=True,
            text=True,
            timeout=120  # 120 second timeout
        )
        return result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return "", "ERROR: Test timed out after 120 seconds"
    except Exception as e:
        return "", f"ERROR: {str(e)}"


def process_single_test(test: Dict, group_name: str, group_dir: Path) -> TestResult:
    """Process a single test (for parallel execution)

    Args:
        test: Test definition dictionary
        group_name: Name of the test group
        group_dir: Directory for group reports

    Returns:
        TestResult with execution results
    """
    test_result = TestResult(
        group=group_name,
        test_num=test['test_num'],
        test_name=test['test_name'],
        user_request=test['user_request']
    )
    test_result.criteria = test['criteria']
    test_result.platform = test['platform']

    # Run test with timing
    test_result.start_time = datetime.now()
    stdout, stderr = run_single_test(test['user_request'])
    test_result.end_time = datetime.now()
    test_result.duration_seconds = (test_result.end_time - test_result.start_time).total_seconds()
    test_result.output = stdout + "\n" + stderr

    # Extract command
    test_result.command_generated = extract_command(stdout)

    # Validate (add group name to test dict for validation)
    test['group'] = group_name
    passed, reason = validate_test(test, stdout, test_result.command_generated)
    test_result.status = "PASS" if passed else "FAIL"
    test_result.failure_reason = reason if not passed else ""

    # Write individual report
    write_test_report(group_dir, test_result)

    # Thread-safe status printing
    with print_lock:
        print(f"  Test {test_result.test_num}: {test_result.test_name[:50]}... {test_result.status} ({test_result.duration_seconds:.1f}s)")

    return test_result
