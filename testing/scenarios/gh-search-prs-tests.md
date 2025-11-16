# gh-search-prs Test Scenarios

## Test 1: Draft Pull Requests

**Description:** Find draft PRs in a repository

**User Request:** "Search for draft pull requests about API changes across GitHub repositories"

**Expected Criteria:**
- Uses `gh search prs`
- Draft filter: `--draft` flag OR query includes `is:draft` (both are valid)
- Query contains API changes or related keywords

**Platform:** All

---

## Test 2: Review Requests

**Description:** Find PRs awaiting your review

**User Request:** "Find open PRs where my review is requested across all repositories"

**Expected Criteria:**
- Review requested: `--review-requested @me`
- State: `--state open`
- Uses `@me` special value

**Platform:** All

---

## Test 3: Merged PRs in Date Range

**Description:** Find merged PRs within date range

**User Request:** "Find PRs merged in 2024 across all of GitHub"

**Expected Criteria:**
- Merged status: `--merged` flag OR query includes `is:merged` (both are valid)
- Date range: `--merged-at "2024-01-01..2024-12-31"` OR query includes `merged:2024-01-01..2024-12-31` (both are valid)
- ISO8601 date format
- Range with `..`

**Platform:** All

---

## Test 4: Review Status Filtering

**Description:** Find approved PRs not yet merged

**User Request:** "Find approved PRs that are still open across GitHub repos"

**Expected Criteria:**
- Review filter: `--review approved`
- State: `--state open`
- Valid review values: approved, changes_requested, required, none

**Platform:** All

---

## Test 5: CI Check Status

**Description:** Find PRs with failing checks

**User Request:** "Find open PRs with failing CI checks across all repos"

**Expected Criteria:**
- Checks filter: `--checks failure`
- State: `--state open`
- Valid check values: pending, success, failure

**Platform:** All

---

## Test 6: Base Branch Filtering

**Description:** Find PRs targeting specific branch

**User Request:** "Find PRs targeting main branch across repositories"

**Expected Criteria:**
- Base filter: `--base main` OR `-B main`
- Valid branch name

**Platform:** All

---

## Test 7: Head Branch Filtering

**Description:** Find PRs from specific branch

**User Request:** "Find PRs from feature-auth branch across GitHub"

**Expected Criteria:**
- Head filter: `--head feature-auth` OR `-H feature-auth`
- Branch name

**Platform:** All

---

## Test 8: Exclude Labels

**Description:** Exclude PRs with specific labels

**User Request:** "Find PRs NOT labeled as WIP across all repos"

**Expected Criteria:**
- Uses `--` flag before query
- Query includes `-label:wip` or `-label:WIP` (case-insensitive label matching)
- Entire query quoted
- Format: `gh search prs -- "query -label:wip"`

**Platform:** Unix/Linux/Mac

---

## Test 9: Author and State

**Description:** Find open PRs by specific author

**User Request:** "Find open pull requests authored by torvalds across all of GitHub"

**Expected Criteria:**
- Author: `--author torvalds`
- State: `--state open`
- No `@` prefix on username

**Platform:** All

---

## Test 10: Multiple Exclusions

**Description:** Exclude multiple labels

**User Request:** "Find PRs NOT labeled as draft or wip across GitHub"

**Expected Criteria:**
- Uses `--` flag
- Query includes `-label:draft -label:wip`
- Multiple exclusions
- Properly quoted

**Platform:** Unix/Linux/Mac

---

## Test 11: Reviewed By User

**Description:** Find PRs reviewed by specific user

**User Request:** "Find PRs reviewed by octocat across all repositories"

**Expected Criteria:**
- Reviewed by: `--reviewed-by octocat`
- No @ prefix on username
- Only @ for @me

**Platform:** All

---

## Test 12: Comment Count

**Description:** Filter by comment activity

**User Request:** "Find highly discussed PRs with over 20 comments across repos"

**Expected Criteria:**
- Comments filter: `--comments ">20"`
- Comparison operator quoted
- NOT unquoted `>20`

**Platform:** All

---

## Test 13: Search in Title

**Description:** Search only in PR titles

**User Request:** "Find PRs with security in the title across GitHub"

**Expected Criteria:**
- Query: `"security in:title"` OR
- Match filter: `--match title`
- Limits search to title field

**Platform:** All

---

## Test 14: Multi-word Label

**Description:** Label with spaces needs inner quotes

**User Request:** "Find PRs labeled as 'needs review' across all repos"

**Expected Criteria:**
- Label syntax: `label:"needs review"`
- Inner quotes around "needs review"
- May need outer quotes for entire query

**Platform:** All

---

## Test 15: PowerShell Exclusion

**Description:** PowerShell requires `--%` for exclusions

**User Request:** "On PowerShell, find PRs NOT labeled as draft across GitHub"

**Expected Criteria:**
- Command starts with `gh --%`
- Includes `--` before query
- Query contains `-label:draft`
- Format: `gh --% search prs -- "-label:draft"`

**Platform:** PowerShell
