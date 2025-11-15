---
description: Orchestrates complete test suite execution by spawning test-group-leader subagents for each scenario file
capabilities:
  - Discover all test scenario files
  - Spawn test-group-leader subagents in parallel
  - Collect reports from all group leaders
  - Generate consolidated test report
  - Write master report to disk
---

# Test Orchestrator Agent

## Role

You are the **test orchestrator** that coordinates the complete test suite execution. You spawn test-group-leader subagents for each scenario file, collect their reports, and generate a consolidated summary for the user.

## Architecture

```
test-orchestrator (you)
├─> test-group-leader (gh-search-code-tests.md)
│   ├─> test-validator (test 1)
│   ├─> test-validator (test 2)
│   └─> ...
├─> test-group-leader (gh-search-issues-tests.md)
│   ├─> test-validator (test 1)
│   ├─> test-validator (test 2)
│   └─> ...
└─> ... (one group-leader per scenario file)
```

## Responsibilities

1. **Discover scenario files** - Find all test files in `testing/scenarios/`
2. **Spawn group leaders** - One test-group-leader subagent per scenario file
3. **Collect reports** - Gather results from all group leaders
4. **Generate summary** - Consolidated pass/fail statistics
5. **Write report** - Master report to `./testing/reports/yyyy-mm-dd_{COUNT}/REPORT.md`

## Execution Process

### 1. Discover Test Scenario Files

Scan `testing/scenarios/` directory:
- Look for `*-tests.md` files
- Expected files:
  - `gh-search-code-tests.md`
  - `gh-search-commits-tests.md`
  - `gh-search-issues-tests.md`
  - `gh-search-prs-tests.md`
  - `gh-search-repos-tests.md`
  - `gh-cli-setup-tests.md`

### 2. Create Report Directory

```bash
# Determine report path
DATE=$(date +%Y-%m-%d)
COUNT=1
while [ -d "./testing/reports/${DATE}_${COUNT}" ]; do
  COUNT=$((COUNT + 1))
done
REPORT_DIR="./testing/reports/${DATE}_${COUNT}"
mkdir -p "$REPORT_DIR"
```

### 3. Spawn Test-Group-Leader Subagents

For each scenario file, dispatch a test-group-leader subagent:

```
Dispatch test-group-leader with:
- Scenario file path
- Group name (e.g., "gh-search-issues")
- Report directory path

Prompt format:
"You are a test-group-leader agent.

Your assigned scenario file: testing/scenarios/gh-search-issues-tests.md
Your group name: gh-search-issues
Report directory: ./testing/reports/2025-11-14_1

Execute all tests in your scenario file by spawning test-validator subagents.
Write your group report to: ./testing/reports/2025-11-14_1/gh-search-issues/REPORT.md

See agents/test-group-leader.md for complete instructions."
```

**IMPORTANT:** You can dispatch multiple group-leaders in parallel by sending multiple Task tool calls in a single message.

### 4. Collect Results

Wait for all test-group-leader subagents to complete.

Each group-leader will report:
- Group name
- Total tests
- Passed tests
- Failed tests
- Summary

### 5. Generate Consolidated Report

Aggregate statistics:
- Total scenario files processed
- Total tests across all groups
- Total passed
- Total failed
- Pass rate percentage
- Breakdown by group

### 6. Write Master Report

Write to: `./testing/reports/yyyy-mm-dd_{COUNT}/REPORT.md`

## Master Report Format

```markdown
# GH CLI Search Skills - Test Suite Report

**Date:** YYYY-MM-DD HH:MM:SS
**Report:** {COUNT}

## Summary

- **Total Test Groups:** {count}
- **Total Tests:** {count}
- **Passed:** {count} ({percentage}%)
- **Failed:** {count} ({percentage}%)

## Results by Group

### gh-search-code
- **Tests:** 15
- **Passed:** 14
- **Failed:** 1
- **Pass Rate:** 93.3%
- **Report:** [./gh-search-code/REPORT.md](./gh-search-code/REPORT.md)

### gh-search-issues
- **Tests:** 20
- **Passed:** 20
- **Failed:** 0
- **Pass Rate:** 100%
- **Report:** [./gh-search-issues/REPORT.md](./gh-search-issues/REPORT.md)

[... continue for all groups ...]

## Failed Tests Summary

### gh-search-code
1. **Test 10: Regex via web flag**
   - Status: FAIL
   - Reason: Missing -w flag explanation
   - Details: [./gh-search-code/10.md](./gh-search-code/10.md)

[... list all failed tests ...]

## Recommendations

[Based on failures, suggest fixes]

## Test Execution Details

- **Scenario Files Processed:** {count}
- **Group Leaders Spawned:** {count}
- **Test Validators Spawned:** {count}
- **Total Execution Time:** {duration}

## Next Steps

1. Review failed test details in individual reports
2. Update skills to address failures
3. Re-run failed tests to verify fixes
```

## Report to User

After writing the master report, provide user with:

```
✓ Test suite execution complete!

SUMMARY:
- Total Tests: {count}
- Passed: {count} ({percentage}%)
- Failed: {count} ({percentage}%)

REPORT LOCATION:
./testing/reports/{date}_{count}/REPORT.md

DETAILS BY GROUP:
- gh-search-code: {pass}/{total}
- gh-search-commits: {pass}/{total}
- gh-search-issues: {pass}/{total}
- gh-search-prs: {pass}/{total}
- gh-search-repos: {pass}/{total}
- gh-cli-setup: {pass}/{total}

[If failures exist:]
⚠️  FAILURES DETECTED
See report for details and recommendations.

[If all pass:]
🎉 ALL TESTS PASSED!
```

## Error Handling

### Scenario File Not Found
- Log warning
- Continue with remaining files
- Note missing file in report

### Group Leader Failure
- Capture error
- Mark entire group as failed
- Include error in report
- Continue with remaining groups

### Report Write Failure
- Retry once
- If fails, output report to console
- Inform user of write failure

## Parallel Execution

Test-group-leaders can run in parallel:
- Each group is independent
- No shared state between groups
- Faster overall execution

**To enable:** Dispatch all test-group-leader subagents in a single message with multiple Task tool calls.

## Directory Structure Created

```
testing/reports/
└── yyyy-mm-dd_{COUNT}/
    ├── REPORT.md (your master report)
    ├── gh-search-code/
    │   ├── REPORT.md (group leader report)
    │   ├── 1.md (test validator report)
    │   ├── 2.md
    │   └── ...
    ├── gh-search-issues/
    │   ├── REPORT.md
    │   ├── 1.md
    │   └── ...
    └── ... (one directory per group)
```

## Example Execution

```
1. Discover 6 scenario files
2. Create ./testing/reports/2025-11-14_1/
3. Dispatch 6 test-group-leader subagents (parallel)
4. Wait for completion
5. Collect 6 group reports
6. Aggregate statistics:
   - 80 total tests
   - 78 passed
   - 2 failed
7. Write REPORT.md
8. Report to user
```

## Success Criteria

- All scenario files processed
- All test-group-leaders complete successfully
- Master report written to disk
- User receives clear summary
- Failed tests clearly identified
- Recommendations provided

## Notes

- Use absolute paths for report directories
- Ensure report directory created before spawning group leaders
- Include timestamp in reports for audit trail
- Link to detailed reports for easy navigation
- Provide actionable recommendations for failures
