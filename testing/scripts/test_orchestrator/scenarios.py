"""Scenario file parsing for test definitions"""

import re
from pathlib import Path
from typing import List, Dict


def parse_scenario_file(filepath: Path) -> List[Dict]:
    """Parse a scenario file and extract test definitions

    Args:
        filepath: Path to the scenario markdown file

    Returns:
        List of test dictionaries with test metadata and criteria
    """
    tests = []
    content = filepath.read_text()

    # Split by test headers
    test_blocks = re.split(r'^## Test (\d+):', content, flags=re.MULTILINE)[1:]

    for i in range(0, len(test_blocks), 2):
        test_num = int(test_blocks[i].strip())
        test_content = test_blocks[i + 1]

        # Extract test name (first line after test number)
        lines = test_content.strip().split('\n')
        test_name = lines[0].strip()

        # Extract fields
        description_match = re.search(r'\*\*Description:\*\*\s*(.+)', test_content)
        request_match = re.search(r'\*\*User Request:\*\*\s*"(.+?)"', test_content)
        platform_match = re.search(r'\*\*Platform:\*\*\s*(.+)', test_content)

        # Extract criteria
        criteria = []
        criteria_section = re.search(r'\*\*Expected Criteria:\*\*\s*\n((?:- .+\n?)+)', test_content)
        if criteria_section:
            criteria = [line.strip()[2:] for line in criteria_section.group(1).strip().split('\n') if line.strip().startswith('-')]

        tests.append({
            'test_num': test_num,
            'test_name': test_name,
            'description': description_match.group(1) if description_match else '',
            'user_request': request_match.group(1) if request_match else '',
            'criteria': criteria,
            'platform': platform_match.group(1).strip() if platform_match else 'All'
        })

    return tests
