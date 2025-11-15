---
name: testing-gh-skills
description: SLASH COMMAND ONLY - Do NOT invoke automatically. Only runs via /test-gh-skills command. Executes Python test orchestrator for 80 tests across 6 skill groups.
---

# Testing GitHub CLI Search Skills

## ⚠️ CRITICAL: Slash Command Only

**This skill should NEVER be invoked automatically.**

**ONLY invoke this skill when:**
- User explicitly runs `/test-gh-skills` slash command
- User explicitly requests "run the test suite"

**DO NOT invoke when:**
- User asks about testing in general
- User asks how to test
- User mentions the word "test" in any context
- You think testing would be helpful
- ANY other scenario

**Why:** Running the full test suite takes ~8 minutes and 80 Claude API calls. This is expensive and should only happen on explicit user request via the slash command.

## Overview

Execute comprehensive test suite for all gh CLI search skills using a **Python test orchestrator**. The script runs 80 tests sequentially, validates responses, and generates detailed reports at multiple levels.

**Core Principle:** Fast, efficient test execution with minimal overhead. Each test runs in a fresh Claude session with only the user request (no test criteria leaked).

**Performance:** ~6 seconds per test, ~8 minutes total for 80 tests.

## When to Use

**ONLY use this skill when user explicitly invokes:**
- `/test-gh-skills` slash command
- Direct request: "run the full test suite"
- Direct request: "execute all tests"

**NEVER use automatically for:**
- Testing a single command manually (use `./testing/scripts/run-single-test.sh` directly)
- Skills haven't been created yet
- Need to write new test scenarios first
- User asks about testing concepts
- User mentions testing in passing

## Architecture

```
python3 testing/scripts/run-all-tests.py
  ├─> Parse all scenario files in testing/scenarios/
  ├─> For each test scenario:
  │   ├─> Execute: ./testing/scripts/run-single-test.sh "<user-request>"
  │   │   └─> claude -p "<user-request>" --allowedTools "Read,Skill"
  │   ├─> Extract command from response
  │   ├─> Validate against expected criteria
  │   └─> Write test report
  ├─> Generate group reports (per scenario file)
  └─> Generate master report (all tests)

THEN (optional but recommended):

test-reviewer agent (agents/test-reviewer.md)
  ├─> Read master report
  ├─> Analyze group reports
  ├─> Sample individual test failures (3-5 examples)
  ├─> Identify failure patterns
  ├─> Perform root cause analysis
  └─> Create REVIEWER-NOTES.md with recommendations

Total: 80 tests across 6 groups (sequential execution) + optional review
```

### Test Groups

1. **gh-cli-setup-tests** (10 tests) - Installation, authentication, troubleshooting
2. **gh-search-code-tests** (15 tests) - Code search with extensions, languages, exclusions
3. **gh-search-commits-tests** (10 tests) - Commit search by author, date, hash
4. **gh-search-issues-tests** (20 tests) - Issue search with labels, assignees, states
5. **gh-search-prs-tests** (15 tests) - PR search with reviews, drafts, checks
6. **gh-search-repos-tests** (10 tests) - Repository search by stars, topics, licenses

### Component Responsibilities

**run-all-tests.py:**
- Discovers all test scenario files in `testing/scenarios/`
- Parses test definitions from markdown
- Executes each test via `run-single-test.sh`
- Validates responses against expected criteria
- Generates 3-level reports (master, group, individual)
- Tracks timing and pass/fail statistics
- Writes to: `./testing/reports/yyyy-mm-dd_{COUNT}/`

**run-single-test.sh:**
- Accepts user request as argument
- Executes Claude CLI with minimal tools (Read, Skill)
- Disables episodic memory for speed
- Bypasses permission prompts
- Requests concise output (command only)
- Returns stdout/stderr for validation

## How to Use

### 1. Run the Test Suite

Execute the Python test orchestrator:

```bash
python3 testing/scripts/run-all-tests.py
```

**Expected output:**
```
GH CLI Search Skills - Test Suite Execution
============================================================
Start time: 2025-11-15 09:00:00

Report directory: /home/aaddrick/source/gh-cli-search/testing/reports/2025-11-15_5

Processing gh-cli-setup-tests...
  Found 10 tests
  Running Test 1: Installation Check Command... PASS
  Running Test 2: Authentication Command... PASS
  ...
  Group complete: 10/10 passed

Processing gh-search-code-tests...
  ...

============================================================
TEST SUITE COMPLETE
============================================================
Total Tests: 80
Passed: 59 (73.8%)
Failed: 21

Execution Time: 480.5 seconds (8.0 minutes)
Average: 6.0 seconds per test

Report location: ./testing/reports/2025-11-15_5/REPORT.md
```

### 2. Review Results

Check the master report at:
```
./testing/reports/yyyy-mm-dd_{COUNT}/REPORT.md
```

This contains:
- Overall pass/fail summary
- Results by group
- Failed tests detail
- Recommendations

### 3. Run Test Reviewer (Recommended)

**After test suite completes**, dispatch a test-reviewer agent to analyze results and produce actionable recommendations.

The test-reviewer will:
- Identify failure patterns across all tests
- Perform root cause analysis
- Distinguish between skill issues, test issues, agent behavior issues, and infrastructure issues
- Provide specific, prioritized recommendations
- Create `REVIEWER-NOTES.md` with comprehensive analysis

**How to invoke:**

Use the Task tool with `subagent_type: general-purpose`:

```
Execute the test-reviewer agent to analyze test suite results.

The test-reviewer agent instructions are located at: agents/test-reviewer.md

Follow all instructions to:
1. Find the latest test report (identify the YYYY-MM-DD_N directory)
2. Read and analyze the master report
3. Review group reports for failing groups
4. Sample individual test failures (3-5 representative examples)
5. Identify failure patterns and root causes
6. Create REVIEWER-NOTES.md with comprehensive analysis

The agent should provide specific, actionable recommendations but NOT make any changes to skills or tests.

Report back when REVIEWER-NOTES.md has been created.
```

**Expected output location:**
```
./testing/reports/yyyy-mm-dd_{COUNT}/REVIEWER-NOTES.md
```

**What the review contains:**
- Executive summary with production-readiness assessment
- Results overview table with status indicators (✅/⚠️/❌)
- Failure patterns with root causes and evidence
- Detailed analysis by group
- Prioritized recommendations (High/Medium/Low)
- Next steps for skill improvements

**When to use test-reviewer:**
- After every full test suite run (to track improvements)
- Before making skill changes (to understand what needs fixing)
- When pass rate is below target (to identify root causes)
- Before releasing skills to production (to validate readiness)

## Report Structure

### Level 1: Master Report
**Location:** `./testing/reports/yyyy-mm-dd_{COUNT}/REPORT.md`
**Generated by:** run-all-tests.py
**Contents:** Overall summary, results by group, failed tests, execution time

### Level 2: Group Reports
**Location:** `./testing/reports/yyyy-mm-dd_{COUNT}/{group-name}/REPORT.md`
**Generated by:** run-all-tests.py
**Contents:** Group summary, individual test results, group-specific pass rate

### Level 3: Individual Test Reports
**Location:** `./testing/reports/yyyy-mm-dd_{COUNT}/{group-name}/{test-number}.md`
**Generated by:** run-all-tests.py
**Contents:** Test details, full response, validation results, pass/fail reason

### Optional: Reviewer Analysis
**Location:** `./testing/reports/yyyy-mm-dd_{COUNT}/REVIEWER-NOTES.md`
**Generated by:** test-reviewer agent (when invoked)
**Contents:** Failure patterns, root cause analysis, prioritized recommendations, next steps

## Key Principles

### Sequential Execution
- Tests run one at a time for clean results
- Each test gets fresh Claude session
- No shared context between tests
- Predictable timing (~6s per test)

### Authentic Testing
- Test subjects receive ONLY user requests (via run-single-test.sh)
- No test criteria given to the test subject
- Validator evaluates responses against criteria
- Skills tested as they would be used naturally

### Comprehensive Reporting
- 3 levels of reports for different audiences
- Master report for quick overview
- Group reports for category-specific issues
- Individual reports for test details and debugging

### Performance Optimizations
- Episodic memory disabled during tests
- Only Read and Skill tools enabled
- Permission prompts bypassed
- Concise output requested (no explanations)
- 120-second timeout per test (rarely needed)

## Test Categories

Tests validate:
- **Syntax:** Correct flag usage, command structure, qualifier syntax
- **Quoting:** Multi-word queries, comparison operators, labels with spaces
- **Exclusions:** `--` flag presence, PowerShell `--% `, exclusions inside quotes
- **Special Values:** `@me` syntax, date formats (ISO8601), comparison operators
- **Platform-Specific:** Unix/Linux/Mac vs PowerShell requirements
- **Edge Cases:** Unusual characters, empty values, boundary conditions
- **Skill Usage:** Validates gh search commands vs gh subcommands

## Success Criteria

**Testing is successful when:**
- All 80 tests execute without errors
- 75%+ pass rate achieved (current baseline: 73.8%)
- Master report generated with timing data
- All group reports generated
- All individual test reports generated
- No test timeouts or crashes

**Target pass rate:** 90%+ (requires skill alignment improvements)

**If tests fail:**
- Review failure details in individual test reports
- Check if skills provide correct syntax
- Verify test criteria match skill documentation
- Fix affected skills or update test expectations
- Re-run full test suite
- Track improvement in pass rate

## Related Documentation

- **Test infrastructure**: `testing/README.md`
- **Test orchestrator**: `testing/scripts/run-all-tests.py`
- **Single test runner**: `testing/scripts/run-single-test.sh`
- **Test reviewer agent**: `agents/test-reviewer.md` - Post-test analysis and recommendations
- **Test scenarios**: `testing/scenarios/*.md`
- **Skills being tested**: `skills/gh-search-*/SKILL.md`, `skills/gh-cli-setup/SKILL.md`

## Common Issues

### Tests Not Running
- Verify Python 3 is installed: `python3 --version`
- Check scenario files exist: `ls testing/scenarios/`
- Ensure run-single-test.sh is executable: `chmod +x testing/scripts/run-single-test.sh`
- Verify Claude CLI is installed: `claude --version`

### Tests Timing Out
- Check if episodic memory is disabled in run-single-test.sh
- Verify permission mode is bypassPermissions
- Increase timeout in run-all-tests.py if needed (currently 120s)

### Reports Not Generated
- Check write permissions: `ls -la testing/reports/`
- Verify directory exists: `mkdir -p testing/reports/`
- Look for Python errors in output

### Low Pass Rate
- Review individual test reports for patterns
- Check if skills were recently modified
- Verify test criteria align with skill documentation
- Consider updating skills to match test expectations
- Common issue: Tests expect query syntax, skills teach flag syntax

### Command Extraction Failures
- Agent response lacks code blocks
- Commands in prose not in ```bash blocks
- Agent explains instead of providing command
- Solution: Update run-single-test.sh prompt for more concise output

## Notes

- Total of 80 test scenarios across 6 skills
- Sequential execution ensures clean test isolation
- Easy to add new test scenarios to scenario files
- Reports provide audit trail of all testing activity
- Run full suite before releasing skill updates
- Test results help identify skill documentation issues
- **Recommended workflow**: Run tests → Review REPORT.md → Dispatch test-reviewer → Implement recommendations → Re-run tests
- Test-reviewer analysis saves time by identifying patterns instead of debugging individual failures
- REVIEWER-NOTES.md provides actionable next steps, not just failure listings
