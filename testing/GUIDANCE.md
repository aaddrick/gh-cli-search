# Testing Guidance & Human Decisions

**Purpose:** This file captures architectural decisions and product philosophy for the gh-cli-search skills testing framework. All automated agents (test-reviewer, product-manager, developer) must read and respect these decisions.

**When to Update:** After any PM halt that requires human feedback, document the decision here before re-running tests.

**Agent Autonomy:** If a decision is already covered in this file, agents should implement fixes autonomously. PM should only halt for NEW architectural questions not covered here.

---

## Agent Autonomy Scope

**What Agents Can Fix Autonomously:**
- Test scenario issues (ambiguous requests, wrong expectations per established philosophy)
- Skill documentation (add examples, clarify syntax, improve completeness)
- Agent definition improvements (better guidelines, clearer instructions)
- Infrastructure bugs (regex issues, validation logic, test orchestration)
- Any fixes that align with decisions already documented in this file

**What Requires Human Judgment (PM should halt):**
- NEW architectural questions not covered by existing decisions in this file
- Fundamental philosophy changes (e.g., "should we completely redesign skills?")
- Trade-offs with no clear winner and no guidance here
- Multiple iterations with no improvement (need human strategy change)

**Key Principle:** If GUIDANCE.md already answers the question, agents implement autonomously. PM only halts for truly new decisions.

---

## Command Selection Philosophy

**Decision Date:** 2025-11-15 (Iteration 1 Halt)

**Context:** PM halted because 55% of failures (12/22) involved agents choosing `gh issue list`/`gh pr list` when tests expected `gh search issues`/`gh search prs`. This revealed an architectural question: should we enforce `gh search` for consistency, or accept scope-optimized commands?

### DECISION: Scope-Optimized Command Selection

**Philosophy:**
- **`gh search`** = Cross-repository searches across the broader GitHub ecosystem
  - Use when searching across multiple repos, organizations, or the entire GitHub platform
  - Examples: "Find issues about authentication across all repos", "Search PRs mentioning Docker in any org"

- **`gh list` commands** = Single-repository, current-context operations
  - Use `gh issue list`, `gh pr list`, `gh repo list` for single-repo operations
  - These are better suited for personal repo management and current-context queries
  - Examples: "Show my open issues", "List PRs in this repo", "Find issues assigned to me"

**Why:** Scope-optimized selection is more efficient and aligns with how real users think about their queries. Forcing `gh search` for single-repo operations would be unnecessarily heavy-handed.

### Implementation Guidelines

**For Test Authors:**
- Tests should be crafted to clearly indicate scope:
  - **Cross-repo scope**: "Find issues about authentication problems across GitHub repos", "Search for PRs that fix similar bugs in other projects"
  - **Single-repo scope**: "Show my open issues", "List PRs I need to review", "Find stale issues in this repo"

**For Test Reviewers:**
- **INVALID failure**: Test says "Find my issues" → Agent uses `gh issue list` → Test expects `gh search issues`
  - **Fix**: Clarify test to specify scope OR accept `gh issue list` as valid
- **VALID failure**: Test says "Find authentication issues across repos" → Agent uses `gh issue list` → Test expects `gh search issues`
  - **Fix**: Agent should have chosen `gh search issues`

**For Skill Authors:**
- Skills should teach BOTH approaches and explain when to use each
- Include decision criteria: "Use `gh search` when query spans multiple repos; use `gh list` for current repo"

**For Developers (Agent):**
- When fixing "search vs list" failures:
  1. Read the user request carefully
  2. Determine if scope is clearly cross-repo or single-repo
  3. If ambiguous → Fix TEST to clarify intent, don't blindly change skill
  4. If clear scope → Fix skill/test to match the scope-optimized philosophy

---

## Test Scenario Design Philosophy

**Decision Date:** 2025-11-15 (Iteration 1 Halt)

**Context:** Many tests propose tasks better served by `gh list` commands but expect `gh search` commands, suggesting test scenarios don't reflect realistic use cases for cross-repository search.

### DECISION: Tests Should Target Cross-Repository Search Use Cases

**Philosophy:**
Tests for `gh search` skills should focus on scenarios where users want to "cast a wide net" across the larger GitHub ecosystem, not manage their personal repos.

**Good Test Scenarios for `gh search issues`:**
- "Find issues about memory leaks in Rust projects"
- "Search for authentication problems across GitHub"
- "Find issues tagged 'help-wanted' in web development repos"
- "Locate similar bug reports in other projects"

**Bad Test Scenarios for `gh search issues`:**
- "Find my issues" → Better served by `gh issue list`
- "Show issues in this repo" → Better served by `gh issue list`
- "List issues assigned to me" → Better served by `gh issue list`

**Same applies to PRs, repos, commits, code:**
- Focus on discovery across GitHub (finding solutions, examples, similar problems)
- Not on managing personal repos (that's what `gh list` commands are for)

**For Test Authors:**
When writing test scenarios:
1. Ask: "Would a user actually want cross-repo results for this query?"
2. Include language-specific or problem-specific context (e.g., "in Python projects", "about Docker")
3. Use phrases indicating breadth: "across repos", "in other projects", "on GitHub"
4. Avoid personal pronouns suggesting single-repo scope: "my issues", "this repo", "our PRs"

---

## Skill Documentation Standards

**Decision Date:** 2025-11-15 (Iteration 1 Halt)

**Context:** Reviewer identified missing documentation for exclusion syntax (`--` separator, query-based exclusions).

### DECISION: No Human Approval Needed for Documentation Fixes

**Philosophy:**
Developer agent has autonomy to implement documentation improvements without human review, including:
- Adding missing syntax examples
- Clarifying existing examples
- Adding `--` separator usage
- Documenting query qualifiers
- Improving clarity and completeness

**Constraints:**
- Don't change skill scope or philosophy (requires human review)
- Don't remove valid approaches (additive improvements only)
- Maintain consistency across all skills
- Follow existing formatting and structure

**For Developer Agent:**
When reviewer recommends documentation updates, implement them directly. Focus on:
1. Adding examples for missing syntax patterns
2. Clarifying ambiguous wording
3. Ensuring completeness (all flags, qualifiers documented)
4. Adding warnings/notes for common pitfalls

---

## Test Expectation Validation

**Decision Date:** 2025-11-15 (Iteration 1 Halt)

**Context:** 12 test cases may have expectations that are too strict or don't align with scope-optimized philosophy.

### DECISION: Question Test Validity Before Fixing Skills

**Philosophy:**
When a test fails, don't assume the agent/skill is wrong. The test expectation might be incorrect.

**Validation Questions:**
1. **Is the test request ambiguous about scope?**
   - If yes → Fix test to clarify (add "across repos" or "in this repo")

2. **Would a real user expect the command the agent chose?**
   - If yes → Test expectation is too strict, fix test

3. **Does the test align with scope-optimized philosophy?**
   - If no → Rewrite test to reflect proper use case

**Process for "Search vs List" Failures:**
1. Read test request
2. Identify intended scope (cross-repo vs single-repo)
3. Verify agent's command choice matches scope
4. If agent correct → Fix test expectations
5. If agent wrong → Fix skill/agent

**For All Agents:**
- Test-Reviewer: Always question test validity in root cause analysis
- Product-Manager: Prioritize test fixes over skill fixes when tests are ambiguous
- Developer: Never blindly implement skill changes without validating test expectations first

---

## Decision Log

### 2025-11-15 - Iteration 1 Halt

**PM Reasoning:** 55% of failures (12/22) involve agents choosing valid `gh list` commands when tests expect `gh search`. This reveals an architectural question requiring human judgment: should we enforce `gh search` for consistency, or accept `gh list` for single-repo efficiency?

**Human Tasks Requested:**
1. ✅ Decide command selection philosophy
2. ✅ Review 12 'search vs list' test cases guidance
3. ✅ Approve skill documentation updates for exclusion syntax
4. ✅ Determine if both approaches should be accepted as valid

**Decisions Made:**
- Command selection: Scope-optimized (search for cross-repo, list for single-repo)
- Test cases: Fix tests to reflect realistic cross-repo search scenarios
- Documentation: Developer has autonomy to fix (no approval needed)
- Both approaches: Accept both but teach when to use each

**Expected Impact:**
- Tests will be rewritten to clarify scope (cross-repo vs single-repo)
- Skills will document both approaches with decision criteria
- Pass rate should improve as ambiguous tests are fixed

**Next Steps:**
- Developer agent should review the 12 failing tests
- Fix test requests to clearly indicate scope
- Update skills to teach scope-based decision making
- Re-run tests to validate improvements

---

## Guidelines for Future Halts

When PM halts for human feedback:

1. **Review PM-NOTES.md** in the halt iteration's report directory
2. **Make decisions** on the architectural/product questions raised
3. **Update this file** with:
   - New section with decision date and context
   - Clear decision statement
   - Implementation guidelines for all agents
   - Add entry to Decision Log
4. **Re-run tests** with updated guidance:
   ```bash
   python3 testing/scripts/run-all-tests.py
   ```

---

**Last Updated:** 2025-11-15
**Last Halt Iteration:** 2025-11-15_1
**Current Pass Rate:** 72.5% (58/80 tests)
