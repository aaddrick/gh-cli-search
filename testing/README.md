# GitHub CLI Search Skills Testing

Comprehensive test suite for validating all gh CLI search skills using a **hierarchical agent architecture**.

## Architecture Overview

```
/test-gh-skills command
  │
  └─> test-orchestrator agent
        ├─> test-group-leader (gh-search-code-tests.md)
        │   ├─> test-validator (test 1) → run-single-test.sh → claude -p "user request"
        │   ├─> test-validator (test 2) → run-single-test.sh → claude -p "user request"
        │   └─> ... (15 tests)
        ├─> test-group-leader (gh-search-commits-tests.md)
        │   └─> ... (10 tests)
        ├─> test-group-leader (gh-search-issues-tests.md)
        │   └─> ... (20 tests)
        ├─> test-group-leader (gh-search-prs-tests.md)
        │   └─> ... (15 tests)
        ├─> test-group-leader (gh-search-repos-tests.md)
        │   └─> ... (10 tests)
        └─> test-group-leader (gh-cli-setup-tests.md)
            └─> ... (10 tests)

Total: 80 tests across 6 groups
```

The testing infrastructure uses interactive subagent hierarchy to execute all 80 test scenarios, verifying that skills produce correct gh CLI commands with proper syntax, quoting, and platform-specific handling.

## Components

### Hierarchical Agent Architecture

The testing system uses a 3-tier agent hierarchy:

```
test-orchestrator (master coordinator)
├─> test-group-leader (per scenario file)
│   └─> test-validator (per individual test)
│       └─> ./testing/scripts/run-single-test.sh
│           └─> claude -p "user request"
```

### Test-Orchestrator Agent

Location: `agents/test-orchestrator.md`

**Purpose:** Master coordinator for entire test suite

**Responsibilities:**
- Discover all test scenario files in testing/scenarios/
- Spawn one test-group-leader per scenario file
- Collect reports from all group leaders
- Generate consolidated master report
- Write to: `./testing/reports/yyyy-mm-dd_{COUNT}/REPORT.md`

### Test-Group-Leader Agent

Location: `agents/test-group-leader.md`

**Purpose:** Manages all tests within one scenario file

**Responsibilities:**
- Parse assigned scenario file
- Extract individual test definitions
- Spawn one test-validator per test
- Collect results from all validators
- Generate group report
- Write to: `./testing/reports/yyyy-mm-dd_{COUNT}/{group-name}/REPORT.md`

### Test-Validator Agent

Location: `agents/test-validator.md`

**Purpose:** Executes single test and evaluates result

**Responsibilities:**
- Execute `./testing/scripts/run-single-test.sh` with user request
- Collect response (no test criteria given to script)
- Evaluate response against expected criteria
- Determine pass/fail
- Write detailed test report
- Write to: `./testing/reports/yyyy-mm-dd_{COUNT}/{group-name}/{test-number}.md`

**Key Principle:** Separation of concerns - test subject doesn't know criteria, validator evaluates

### Test Scenarios

Location: `testing/scenarios/`

**Files:**
- `gh-search-code-tests.md` - 15 tests for code search
- `gh-search-commits-tests.md` - 10 tests for commit search
- `gh-search-issues-tests.md` - 20 tests for issue search
- `gh-search-prs-tests.md` - 15 tests for PR search
- `gh-search-repos-tests.md` - 10 tests for repository search
- `gh-cli-setup-tests.md` - 10 tests for setup/troubleshooting

**Total:** 80 test scenarios

## Running Tests

### Full Test Suite

Run the complete test suite via slash command:

```bash
/test-gh-skills
```

This spawns the test-orchestrator agent which:
1. Discovers all scenario files
2. Spawns test-group-leader for each file (can run in parallel)
3. Each group-leader spawns test-validators for each test (can run in parallel)
4. Generates comprehensive reports at all levels

**Process Flow:**
```
/test-gh-skills
  └─> test-orchestrator
      ├─> test-group-leader (gh-search-code)
      │   ├─> test-validator (test 1) → run-single-test.sh
      │   ├─> test-validator (test 2) → run-single-test.sh
      │   └─> ... (15 tests)
      ├─> test-group-leader (gh-search-issues)
      │   └─> ... (20 tests)
      └─> ... (6 groups total)
```

**Reports Generated:**
- Master: `./testing/reports/2025-11-14_1/REPORT.md`
- Groups: `./testing/reports/2025-11-14_1/{group}/REPORT.md`
- Tests: `./testing/reports/2025-11-14_1/{group}/{number}.md`

### Manual Single Test

To test a single command manually (outside the full test suite):

```bash
./testing/scripts/run-single-test.sh "Find my open issues NOT labeled as bug"
```

This executes Claude with ONLY the user request to see how skills are applied naturally, without any test criteria hints.

## Test Categories

### Syntax Tests
- Correct flag usage
- Proper command structure
- Valid qualifier syntax

### Quoting Tests
- Multi-word queries quoted
- Comparison operators quoted
- Labels with spaces handled
- Complex query quoting

### Exclusion Tests
- `--` flag for exclusions
- PowerShell `--% ` handling
- Exclusions inside quotes
- Multiple exclusions

### Special Values Tests
- `@me` syntax
- Date formats (ISO8601)
- Comparison operators
- Range syntax (`..`)

### Platform-Specific Tests
- Unix/Linux/Mac requirements
- PowerShell requirements
- Cross-platform compatibility

### Edge Case Tests
- Unusual characters
- Empty values
- Boundary conditions

## Report Structure

The hierarchical testing architecture generates reports at three levels:

### Level 1: Master Report

**Location:** `./testing/reports/yyyy-mm-dd_{COUNT}/REPORT.md`

**Generated by:** test-orchestrator

**Contents:**
- Overall summary (total tests, pass/fail, percentage)
- Results by group
- Failed tests summary across all groups
- Recommendations
- Links to all group reports

**Example:**
```markdown
# GH CLI Search Skills - Test Suite Report

**Date:** 2025-11-14 15:30:00
**Report:** 1

## Summary
- **Total Test Groups:** 6
- **Total Tests:** 80
- **Passed:** 78 (97.5%)
- **Failed:** 2 (2.5%)

## Results by Group

### gh-search-code
- **Tests:** 15
- **Passed:** 14
- **Failed:** 1
- **Report:** [./gh-search-code/REPORT.md](./gh-search-code/REPORT.md)

[... other groups ...]

## Failed Tests Summary
[Details on each failure across all groups]

## Recommendations
[Actionable suggestions based on failures]
```

### Level 2: Group Reports

**Location:** `./testing/reports/yyyy-mm-dd_{COUNT}/{group-name}/REPORT.md`

**Generated by:** test-group-leader

**Contents:**
- Group summary
- Individual test results
- Failed tests detail for this group
- Prompts given to each test-validator
- Responses from each test-validator
- Group-specific recommendations
- Links to individual test reports

### Level 3: Individual Test Reports

**Location:** `./testing/reports/yyyy-mm-dd_{COUNT}/{group-name}/{test-number}.md`

**Generated by:** test-validator

**Contents:**
- Test details (name, description, platform)
- Instructions given to run-single-test.sh
- Full response from run-single-test.sh
- Expected criteria
- Validation results (criterion by criterion)
- Overall assessment
- Detailed findings
- Recommendations
- Execution metadata

## Test Scenario Format

Each test scenario includes:

```markdown
## Test N: Test Name

**Description:** What this test validates

**User Request:** "Simulated user query"

**Expected Criteria:**
- Criterion 1
- Criterion 2
- ...

**Platform:** Unix/Linux/Mac, PowerShell, or All
```

## Writing New Tests

When adding new tests:

1. **Identify what to test** - New feature, edge case, common mistake
2. **Write clear description** - What does this test validate?
3. **Simulate user request** - Realistic user query
4. **Define success criteria** - Specific, measurable expectations
5. **Specify platform** - Unix/Mac, PowerShell, or All
6. **Add to scenario file** - Keep organized by skill

## Maintaining Tests

### When to Update Tests

- Skill documentation changes
- New features added
- Bugs discovered
- Edge cases identified
- Common mistakes found

### Test Maintenance Checklist

- [ ] Review test scenarios quarterly
- [ ] Add tests for new features
- [ ] Update tests when skills change
- [ ] Remove obsolete tests
- [ ] Keep expected criteria current
- [ ] Verify all tests still pass

## Success Criteria

**Testing is successful when:**
- All 80 tests execute
- 100% pass rate achieved
- No false positives/negatives
- Clear, actionable feedback for failures
- Skills are production-ready

## Troubleshooting Tests

### Test-Validator Not Found

Ensure agent file exists: `agents/test-validator.md`

### Test Scenarios Not Loading

Check files exist in: `testing/scenarios/`

### Tests Failing Unexpectedly

1. Review skill documentation for recent changes
2. Check expected criteria in test scenario
3. Verify test-validator agent is functioning
4. Re-run individual test to diagnose

### Subagent Dispatch Issues

Ensure testing-gh-skills skill is being used correctly.

## Best Practices

1. **Run tests before releases** - Always validate before publishing
2. **Fix failures immediately** - Don't ship with failing tests
3. **Update tests with skills** - Keep tests and skills in sync
4. **Test edge cases** - Not just happy paths
5. **Document test rationale** - Why does this test exist?
6. **Keep tests independent** - No dependencies between tests
7. **Make tests repeatable** - Same input = same result

## Benefits of Hierarchical Architecture

### Parallel Execution
- **Group level:** Multiple scenario files can be tested simultaneously
- **Test level:** Multiple tests within a group can run concurrently
- **Result:** Much faster overall execution compared to sequential

### Clear Separation of Concerns
- **test-orchestrator:** Master coordination, no test details
- **test-group-leader:** Group coordination, no individual test execution
- **test-validator:** Test execution and evaluation only

### Comprehensive Reporting
- **Three-level reports:** Master, group, and individual test
- **Traceability:** Easy to drill down from summary to details
- **Audit trail:** Complete record of prompts, responses, and evaluations

### Authentic Testing
- Test subjects (run-single-test.sh) receive ONLY user requests
- No test criteria leakage
- Skills tested as they would be used naturally

### Scalability
- Easy to add new scenario files
- Easy to add new tests to existing groups
- No changes needed to agent hierarchy

## Related Documentation

- Test-orchestrator agent: `agents/test-orchestrator.md`
- Test-group-leader agent: `agents/test-group-leader.md`
- Test-validator agent: `agents/test-validator.md`
- Test scenarios: `testing/scenarios/`
- Skills being tested: `skills/gh-search-*/`

## Statistics

- **Total Test Scenarios:** 80
- **Skills Tested:** 6
- **Test Categories:** 6
- **Platform Variants:** Unix/Mac, PowerShell, All
- **Average Tests per Skill:** 13

## Contributing New Tests

To contribute new test scenarios:

1. Identify gap in test coverage
2. Write test following format
3. Add to appropriate scenario file
4. Run test to verify it works
5. Update this README if needed
6. Commit with clear description

Good test contributions:
- Cover edge cases
- Test common mistakes
- Verify platform differences
- Validate new features
- Catch regressions
