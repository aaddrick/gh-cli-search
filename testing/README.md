# GitHub CLI Search Skills Testing

Comprehensive automated test suite for validating all gh CLI search skills with **parallel execution, automated review, and intelligent iteration**.

## Architecture Overview

```
python3 testing/scripts/run-all-tests.py [--workers N] [--verbose]
  │
  ├─> Iteration Loop (max 5 iterations)
  │   │
  │   ├─> Test Execution (Parallel)
  │   │   ├─> Parse scenario files
  │   │   ├─> ThreadPoolExecutor (default: 8 workers)
  │   │   │   ├─> Worker 1: run-single-test.sh → claude -p "user request"
  │   │   │   ├─> Worker 2: run-single-test.sh → claude -p "user request"
  │   │   │   ├─> Worker 3-8: ... (parallel execution)
  │   │   └─> Generate reports (REPORT.md + individual test reports)
  │   │
  │   ├─> Test-Reviewer Agent (Headless)
  │   │   ├─> Read test results and previous PM-NOTES (if available)
  │   │   ├─> Analyze failure patterns
  │   │   ├─> Perform root cause analysis
  │   │   └─> Create REVIEWER-NOTES.md (with git commit ID)
  │   │
  │   ├─> Product-Manager Agent (Headless)
  │   │   ├─> Read test results + REVIEWER-NOTES + previous PM-NOTES
  │   │   ├─> Analyze improvement trajectory
  │   │   ├─> Decide: RERUN or HALT
  │   │   ├─> Create PM-NOTES.md (with git commit ID)
  │   │   └─> Return JSON decision
  │   │       ├─> "rerun" → Developer agent → Next iteration
  │   │       └─> "halt" → Wait for human feedback
  │   │
  │   └─> Developer Agent (Headless, if RERUN decision)
  │       ├─> Read REVIEWER-NOTES.md + PM-NOTES.md
  │       ├─> Implement recommended fixes
  │       ├─> Update skill documentation
  │       ├─> Fix test validation bugs
  │       └─> Create DEV-NOTES.md

Total: 80 tests across 6 groups, with automated review, decision-making, and fixes
```

The testing infrastructure uses a modular Python orchestrator (`test_orchestrator` package) with parallel execution, followed by automated review agents that analyze results, make intelligent iteration decisions, and automatically implement fixes when appropriate.

## Components

### 1. Test Orchestrator

**Entry Point:** `testing/scripts/run-all-tests.py`

**Package:** `testing/scripts/test_orchestrator/` (modular architecture)

**Purpose:** Parallel test execution, iteration management, and automated improvement

**Module Structure:**
- `orchestration.py` - Main execution loop and iteration management
- `execution.py` - Individual test execution logic
- `validation.py` - Test output validation and command extraction
- `reporting.py` - Multi-level report generation
- `scenarios.py` - Scenario file parsing
- `models.py` - Data structures (TestResult, etc.)
- `config.py` - Paths and configuration constants
- `agents/` - Agent invocation modules (test_reviewer, product_manager, developer)

**Responsibilities:**
- Parse all test scenario files in `testing/scenarios/`
- Execute tests in parallel using ThreadPoolExecutor (configurable workers)
- Validate responses against expected criteria
- Generate comprehensive reports at multiple levels
- Capture git commit ID for traceability
- Manage iteration loop (up to 5 iterations)
- Invoke test-reviewer, product-manager, and developer agents automatically
- Write to: `./testing/reports/yyyy-mm-dd_{COUNT}/`

**Key Features:**
- **Parallel execution:** 8 workers by default (configurable with `--workers`)
- **Modular architecture:** Clean separation of concerns, maintainable codebase
- **Iteration tracking:** Separate directories for each test run
- **Commit traceability:** Git commit ID captured and added to all agent notes
- **Automatic agents:** Reviewer, PM, and developer run after each test execution
- **Verbose mode:** Real-time agent output for debugging
- **Safety limits:** Maximum 5 iterations to prevent infinite loops

**Command-Line Options:**
```bash
python3 testing/scripts/run-all-tests.py                # Default: 8 workers, with review
python3 testing/scripts/run-all-tests.py --workers 16   # Use 16 parallel workers
python3 testing/scripts/run-all-tests.py --no-review    # Skip all automated agents
python3 testing/scripts/run-all-tests.py --no-pm        # Run reviewer but skip PM decision
python3 testing/scripts/run-all-tests.py --no-dev       # Skip developer agent (no auto-fixes)
python3 testing/scripts/run-all-tests.py --verbose      # Show real-time agent output
```

### 2. Test-Reviewer Agent

**Location:** `agents/test-reviewer.md`

**Purpose:** Automated analysis of test results

**Invocation:** Headless agent via `claude -p` after test execution

**Responsibilities:**
- Read master REPORT.md for overall statistics
- Read previous PM-NOTES.md (if available) for context
- Analyze group reports for failing groups
- Sample 3-5 representative test failures for deep dive
- Identify failure patterns across all tests
- Perform root cause analysis
- Distinguish between skill issues, test issues, agent behavior, and infrastructure
- Question test validity before assuming skills are wrong
- Create REVIEWER-NOTES.md with comprehensive analysis

**Output:** `./testing/reports/yyyy-mm-dd_{COUNT}/REVIEWER-NOTES.md`

**Timeout:** 5 minutes

### 3. Product-Manager Agent

**Location:** `agents/product-manager.md`

**Purpose:** Intelligent decision-making about test iteration

**Invocation:** Headless agent via `claude -p --output-format json` after test-reviewer

**Responsibilities:**
- Read test results (REPORT.md)
- Read reviewer analysis (REVIEWER-NOTES.md)
- Read ALL previous PM-NOTES.md files (if iteration 2+)
- Analyze improvement trajectory across iterations
- Evaluate whether to continue iterating or halt
- Consider: pass rate zones, root cause clarity, fixability, trajectory patterns
- Create PM-NOTES.md with decision rationale
- Return JSON decision: `{"action": "rerun"|"halt", "reasoning": "...", "confidence": "high"|"medium"|"low"}`

**Output:**
- `./testing/reports/yyyy-mm-dd_{COUNT}/PM-NOTES.md`
- JSON decision parsed by orchestrator script

**Timeout:** 3 minutes

**Decision Zones:**
- **< 40%:** HALT (critical issues need human review)
- **40-60%:** Evaluate trajectory and root causes carefully
- **60-85%:** Prime zone for automated improvement
- **> 85%:** Usually HALT (diminishing returns)

**Trajectory Analysis:**
- **Accelerating:** Each iteration improves more → Continue
- **Linear:** Consistent improvement → Continue if far from goal
- **Diminishing:** Each iteration improves less → Consider overall direction, not single low yield
- **Plateauing:** No significant change across multiple iterations → HALT
- **Declining:** Getting worse → HALT immediately

### 4. Developer Agent

**Location:** `agents/developer.md`

**Purpose:** Automated implementation of fixes based on reviewer/PM recommendations

**Invocation:** Headless agent via `claude -p` after PM decides to RERUN

**Responsibilities:**
- Read REVIEWER-NOTES.md and PM-NOTES.md for context
- Implement high-priority fixes identified by reviewer
- Update skill documentation to address failures
- Fix test validation bugs if applicable
- Make targeted changes to improve pass rate
- Create DEV-NOTES.md documenting changes made
- Commit changes with clear descriptions

**Output:**
- `./testing/reports/yyyy-mm-dd_{COUNT}/DEV-NOTES.md`
- Code changes committed to repository

**Timeout:** 10 minutes

**When It Runs:**
- Only when PM decides RERUN (not on HALT)
- Can be skipped with `--no-dev` flag
- Runs between PM decision and next test iteration

**Safety Features:**
- Reads testing/GUIDANCE.md for human decisions and constraints
- Questions test validity before changing skills
- Makes minimal, targeted changes
- Documents all changes in DEV-NOTES.md
- Commits changes for traceability

### 5. Single Test Runner

**Location:** `testing/scripts/run-single-test.sh`

**Purpose:** Execute a single test in isolation

**Usage:**
```bash
./testing/scripts/run-single-test.sh "Find my open issues NOT labeled as bug"
```

**Behavior:**
- Accepts user request as argument
- Executes `claude -p` with minimal tools (Read, Skill)
- Disables episodic memory for speed
- Bypasses permission prompts
- Requests concise output (command only)
- Returns stdout/stderr for validation
- 120-second timeout per test

**Key Principle:** Test subject receives ONLY the user request, no test criteria hints.

### 6. Test Scenarios

**Location:** `testing/scenarios/`

**Files:**
- `gh-search-code-tests.md` - 15 tests for code search
- `gh-search-commits-tests.md` - 10 tests for commit search
- `gh-search-issues-tests.md` - 20 tests for issue search
- `gh-search-prs-tests.md` - 15 tests for PR search
- `gh-search-repos-tests.md` - 10 tests for repository search
- `gh-cli-setup-tests.md` - 10 tests for setup/troubleshooting

**Total:** 80 test scenarios

## Running Tests

### Full Test Suite with Automation

Run the complete test suite with default settings:

```bash
python3 testing/scripts/run-all-tests.py
```

**What happens:**
1. **Test Run 1:** Execute 80 tests in parallel (8 workers)
2. **Test-Reviewer:** Analyze results, create REVIEWER-NOTES.md (with commit ID)
3. **Product-Manager:** Review analysis, decide rerun/halt, create PM-NOTES.md (with commit ID)
4. **If RERUN:** Developer agent implements fixes, then iteration 2 begins in new directory
5. **If HALT:** Stop and display human tasks needed

**Process Flow:**
```
Test Run 1: testing/reports/2025-11-15_1/
├─ Git Commit: abc1234
├─ Test Execution (80 tests, ~1-2 minutes with 8 workers)
├─ REPORT.md
├─ REVIEWER-NOTES.md (automated analysis, starts with commit ID)
├─ PM-NOTES.md (decision: RERUN, starts with commit ID)
└─ DEV-NOTES.md (developer agent implements fixes)

Test Run 2: testing/reports/2025-11-15_2/
├─ Git Commit: def5678 (includes developer fixes)
├─ Test Execution (80 tests, ~1-2 minutes)
├─ REPORT.md
├─ REVIEWER-NOTES.md (reads previous PM-NOTES for context)
└─ PM-NOTES.md (decision: HALT - 95% pass rate achieved)

Final Summary:
- Total test runs: 2
- Final pass rate: 95%
- Total time: ~12-18 minutes (tests + agents)
- Human tasks: [listed by PM]
```

### Advanced Options

```bash
# Use 16 parallel workers (faster on powerful machines)
python3 testing/scripts/run-all-tests.py --workers 16

# Skip all automated agents (just run tests)
python3 testing/scripts/run-all-tests.py --no-review

# Run reviewer but skip PM decision (halt after one test run)
python3 testing/scripts/run-all-tests.py --no-pm

# Run reviewer and PM but skip developer agent (no automated fixes)
python3 testing/scripts/run-all-tests.py --no-dev

# Show real-time agent output for debugging
python3 testing/scripts/run-all-tests.py --verbose
```

### Manual Single Test

To test a single command manually (outside the full suite):

```bash
./testing/scripts/run-single-test.sh "Find my open issues NOT labeled as bug"
```

This executes Claude with ONLY the user request to see how skills are applied naturally.

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

The testing system generates reports at six levels:

### Level 1: Master Report

**Location:** `./testing/reports/yyyy-mm-dd_{COUNT}/REPORT.md`

**Generated by:** run-all-tests.py

**Contents:**
- Overall summary (total tests, pass/fail, percentage)
- Results by group
- Failed tests summary across all groups
- Execution time and performance metrics
- Links to all group reports

### Level 2: Group Reports

**Location:** `./testing/reports/yyyy-mm-dd_{COUNT}/{group-name}/REPORT.md`

**Generated by:** run-all-tests.py

**Contents:**
- Group summary
- Individual test results
- Failed tests detail for this group
- Links to individual test reports

### Level 3: Individual Test Reports

**Location:** `./testing/reports/yyyy-mm-dd_{COUNT}/{group-name}/{test-number}.md`

**Generated by:** run-all-tests.py

**Contents:**
- Test details (name, description, platform)
- User request given to run-single-test.sh
- Full response from run-single-test.sh
- Command extracted from response
- Expected criteria
- Validation results (criterion by criterion)
- Pass/fail status with reasoning

### Level 4: Reviewer Analysis (Automatic)

**Location:** `./testing/reports/yyyy-mm-dd_{COUNT}/REVIEWER-NOTES.md`

**Generated by:** test-reviewer agent (automatic headless invocation)

**Contents:**
- **Git Commit ID** (first line for traceability)
- Executive summary with production-readiness assessment
- Results overview table with status indicators (✅/⚠️/❌)
- Failure patterns with root causes and evidence
- Detailed analysis by group
- Prioritized recommendations (High/Medium/Low)
- Test examples in appendix
- Next steps for improvements

### Level 5: Product Manager Decision (Automatic)

**Location:** `./testing/reports/yyyy-mm-dd_{COUNT}/PM-NOTES.md`

**Generated by:** product-manager agent (automatic headless invocation)

**Contents:**
- **Git Commit ID** (first line for traceability)
- Decision: RERUN or HALT
- Confidence level (high/medium/low)
- Executive summary
- Test results analysis with pass rate
- Reviewer's key findings summary
- Decision rationale with supporting factors
- Risk assessment
- Historical context (if test run 2+)
- Improvement trajectory analysis
- Recommended actions or human tasks
- Expected outcomes (if rerun)

### Level 6: Developer Implementation (Automatic, if RERUN)

**Location:** `./testing/reports/yyyy-mm-dd_{COUNT}/DEV-NOTES.md`

**Generated by:** developer agent (automatic headless invocation after PM RERUN decision)

**Contents:**
- Summary of fixes implemented
- Files changed with descriptions
- Rationale for each change
- Testing approach used (if applicable)
- Commit references
- Warnings or notes for human review
- Next steps or follow-up items

## Iteration System

### How Iterations Work

1. **Test Run 1:** Initial test run in `yyyy-mm-dd_1/` directory with commit ID capture
2. **After tests:** Reviewer analyzes → PM decides → Developer implements fixes (if RERUN)
3. **If RERUN:** Developer agent makes fixes, commits changes, then Test Run 2 in new directory (`yyyy-mm-dd_2/`)
4. **Test Run 2+:** Agents read all previous notes for full context, new commit ID captured
5. **Repeat:** Up to 5 test runs maximum
6. **If HALT:** Stop and show human tasks

### Test Run Directories

Each test run gets its own directory with incrementing count:

```
testing/reports/
├─ 2025-11-15_1/              # Test Run 1
│  ├─ Git Commit: abc1234
│  ├─ REPORT.md
│  ├─ REVIEWER-NOTES.md       # Starts with "**Git Commit:** abc1234"
│  ├─ PM-NOTES.md             # Decision: RERUN, starts with commit ID
│  ├─ DEV-NOTES.md            # Developer fixes implemented
│  └─ [group dirs]/
├─ 2025-11-15_2/              # Test Run 2 (after developer fixes)
│  ├─ Git Commit: def5678
│  ├─ REPORT.md
│  ├─ REVIEWER-NOTES.md       # Reads ../2025-11-15_1/PM-NOTES.md
│  ├─ PM-NOTES.md             # Decision: RERUN
│  ├─ DEV-NOTES.md
│  └─ [group dirs]/
└─ 2025-11-15_3/              # Test Run 3
   ├─ Git Commit: ghi9012
   ├─ REPORT.md
   ├─ REVIEWER-NOTES.md       # Reads all previous PM-NOTES
   ├─ PM-NOTES.md             # Decision: HALT
   └─ [group dirs]/
```

**Note:** Each script execution creates new directories with incrementing counts. Directories from different script runs persist, allowing historical comparison.

### PM Decision Logic

The product-manager agent considers:

1. **Pass Rate Zones**
   - < 40%: Fundamental issues → HALT
   - 40-60%: Borderline → Evaluate carefully
   - 60-85%: Sweet spot → Usually RERUN
   - > 85%: Diminishing returns → Usually HALT

2. **Root Cause Clarity**
   - Clear mechanical fixes → RERUN
   - Ambiguous or design decisions needed → HALT

3. **Improvement Trajectory** (for iteration 2+)
   - Overall direction matters more than single low-yield iteration
   - Looks at pattern across multiple iterations
   - Accelerating/linear → Continue
   - Consistent declining trend → HALT

4. **Iteration Count**
   - Iteration 1: Liberal with RERUN
   - Iteration 2-3: Evaluate trajectory
   - Iteration 4-5: Conservative, lean toward HALT
   - After 5: Always HALT

### Example Iteration Flow

```
Iteration 1: 41.2% pass → PM: "Clear fixes identified, expect +15%" → RERUN
Iteration 2: 57.3% pass (+16.1%, exceeds prediction) → PM: "Good progress, expect +10%" → RERUN
Iteration 3: 58.9% pass (+1.6%, below prediction but still improving) → PM: "Minor gain but pattern unclear, expect +5%" → RERUN
Iteration 4: 75.2% pass (+16.3%, unexpected jump!) → PM: "Strong recovery, trajectory positive" → RERUN
Iteration 5: 78.1% pass (+2.9%) → PM: "At max iterations, good enough at 78%" → HALT
```

Note: PM evaluates overall direction, not just one low-yield iteration.

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

## Performance

### Execution Speed

**Sequential (old):** ~8 minutes for 80 tests (~6 seconds per test)

**Parallel (current):**
- 8 workers (default): ~1-2 minutes for 80 tests
- 16 workers: ~45-90 seconds for 80 tests (on powerful machines)

**Full Test Run with Agents:**
- Test execution: 1-2 minutes (8 workers)
- Test-reviewer: 3-5 minutes
- Product-manager: 1-3 minutes
- Developer agent: 5-10 minutes (if RERUN)
- **Total per test run:** 10-20 minutes (with developer), 5-10 minutes (without)

**Multi-Run Example:**
- 3 test runs with development: ~30-60 minutes total
- Includes all automated review, decision-making, and fix implementation

## Writing New Tests

When adding new tests:

1. **Identify what to test** - New feature, edge case, common mistake
2. **Write clear description** - What does this test validate?
3. **Simulate user request** - Realistic user query
4. **Define success criteria** - Specific, measurable expectations
5. **Specify platform** - Unix/Mac, PowerShell, or All
6. **Add to scenario file** - Keep organized by skill
7. **Run test manually first** - Verify it works as expected
8. **Run full suite** - Ensure no regressions

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
- [ ] Run full suite to verify

## Success Criteria

**Testing is successful when:**
- All 80 tests execute without errors
- Pass rate ≥ 85% (target: 90%+)
- No false positives/negatives
- Clear, actionable feedback for failures
- Automated agents provide valuable insights
- PM makes sensible rerun/halt decisions
- Skills are production-ready

## Troubleshooting

### Tests Not Running

**Issue:** Script fails to start

**Solutions:**
- Verify Python 3 is installed: `python3 --version`
- Check scenario files exist: `ls testing/scenarios/`
- Ensure run-single-test.sh is executable: `chmod +x testing/scripts/run-single-test.sh`
- Verify Claude CLI is installed: `claude --version`

### Tests Timing Out

**Issue:** Individual tests exceed 120s timeout

**Solutions:**
- Check if episodic memory is disabled in run-single-test.sh
- Verify permission mode is bypassPermissions
- Increase timeout in run-all-tests.py if needed

### Reviewer Agent Fails

**Issue:** Test-reviewer doesn't complete

**Solutions:**
- Check agent file exists: `agents/test-reviewer.md`
- Verify report directory has REPORT.md
- Check Claude CLI logs for errors
- Try running with --no-review to skip

### PM Agent Fails

**Issue:** Product-manager doesn't complete or returns invalid JSON

**Solutions:**
- Check agent file exists: `agents/product-manager.md`
- Verify REVIEWER-NOTES.md was created
- Check for JSON parsing errors in script output
- Try running with --no-pm to skip

### Iteration Loop Not Working

**Issue:** Tests don't iterate when PM says RERUN

**Solutions:**
- Check PM-NOTES.md was created
- Verify JSON output from PM is valid
- Look for errors in script output
- Check iteration count hasn't hit max (5)

## Best Practices

1. **Run tests before releases** - Always validate before publishing
2. **Fix failures immediately** - Don't ship with failing tests
3. **Update tests with skills** - Keep tests and skills in sync
4. **Trust the automated agents** - Reviewer and PM have good judgment
5. **Review PM-NOTES** - Understand why decisions were made
6. **Test edge cases** - Not just happy paths
7. **Document test rationale** - Why does this test exist?
8. **Keep tests independent** - No dependencies between tests
9. **Make tests repeatable** - Same input = same result
10. **Monitor iteration patterns** - Learn from multi-iteration runs

## Benefits of Current Architecture

### Modular Design
- **Clean separation** of concerns across 11 focused modules
- **Maintainable** codebase with clear responsibilities
- **Extensible** architecture for adding new agents or features
- **Testable** components with well-defined interfaces

### Parallel Execution
- **85% faster** than sequential execution (8 workers)
- Configurable worker count for different machine capabilities
- Thread-safe output handling
- Efficient resource utilization

### Automated Intelligence
- **Test-reviewer** identifies patterns humans might miss
- **Product-manager** makes data-driven iteration decisions
- **Developer agent** implements fixes automatically
- **Historical context** improves decision quality over test runs
- Frees humans from tedious analysis and repetitive fixes

### Full Traceability
- **Git commit ID** captured at test start
- **Six-level reports** (master, group, individual, reviewer, PM, developer)
- **Complete audit trail** from test results to implemented fixes
- **Historical comparison** across multiple test runs

### Authentic Testing
- Test subjects receive ONLY user requests
- No test criteria leakage
- Skills tested as they would be used naturally
- Real-world usage patterns validated

### Intelligent Iteration
- **Self-improving** through automated reruns with fixes
- **Safety limits** prevent infinite loops (max 5 runs)
- **Trajectory analysis** considers overall patterns
- **Diminishing returns detection** stops at right time
- **Automated fixes** reduce human intervention needed

## Related Documentation

- Test orchestrator entry point: `testing/scripts/run-all-tests.py`
- Orchestrator package: `testing/scripts/test_orchestrator/`
- Orchestration logic: `testing/scripts/test_orchestrator/orchestration.py`
- Agent invocations: `testing/scripts/test_orchestrator/agents/`
- Test-reviewer agent: `agents/test-reviewer.md`
- Product-manager agent: `agents/product-manager.md`
- Developer agent: `agents/developer.md`
- Single test runner: `testing/scripts/run-single-test.sh`
- Test scenarios: `testing/scenarios/`
- Skills being tested: `skills/gh-search-*/`, `skills/gh-cli-setup/`
- Refactor documentation: `docs/plans/2025-11-15-refactor-orchestrator-modules.md`

## Statistics

- **Total Test Scenarios:** 80
- **Skills Tested:** 6
- **Test Categories:** 6
- **Platform Variants:** Unix/Mac, PowerShell, All
- **Average Tests per Skill:** 13
- **Parallel Workers:** 8 (default), configurable up to 16+
- **Max Test Runs:** 5 per script execution
- **Orchestrator Modules:** 11 (modular architecture)
- **Agent Types:** 3 (test-reviewer, product-manager, developer)
- **Typical Test Run Time:** 10-20 minutes (with all agents)
- **Target Pass Rate:** 90-95%

## Contributing New Tests

To contribute new test scenarios:

1. Identify gap in test coverage
2. Write test following format
3. Add to appropriate scenario file
4. Run test manually to verify
5. Run full suite to check for regressions
6. Update this README if needed
7. Commit with clear description

Good test contributions:
- Cover edge cases
- Test common mistakes
- Verify platform differences
- Validate new features
- Catch regressions
- Include clear rationale
