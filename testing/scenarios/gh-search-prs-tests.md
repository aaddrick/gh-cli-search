# gh-search-prs Test Scenarios

## Test 1: Draft Pull Requests

**Description:** Find draft PRs in a repository

**User Request:** "Find all draft pull requests in cli/cli repo"

**Expected Criteria:**
- Uses `gh search prs`
- Draft filter: `--draft` flag
- Repository: `--repo cli/cli`

**Platform:** All

---

## Test 2: Review Requests

**Description:** Find PRs awaiting your review

**User Request:** "Find open PRs where my review is requested"

**Expected Criteria:**
- Review requested: `--review-requested @me`
- State: `--state open`
- Uses `@me` special value

**Platform:** All

---

## Test 3: Merged PRs in Date Range

**Description:** Find merged PRs within date range

**User Request:** "Find PRs merged in 2024"

**Expected Criteria:**
- Merged flag: `--merged`
- Merged date: `--merged-at "2024-01-01..2024-12-31"`
- ISO8601 date format
- Range with `..`

**Platform:** All

---

## Test 4: Review Status Filtering

**Description:** Find approved PRs not yet merged

**User Request:** "Find approved PRs that are still open"

**Expected Criteria:**
- Review filter: `--review approved`
- State: `--state open`
- Valid review values: approved, changes_requested, required, none

**Platform:** All

---

## Test 5: CI Check Status

**Description:** Find PRs with failing checks

**User Request:** "Find open PRs with failing CI checks"

**Expected Criteria:**
- Checks filter: `--checks failure`
- State: `--state open`
- Valid check values: pending, success, failure

**Platform:** All

---

## Test 6: Base Branch Filtering

**Description:** Find PRs targeting specific branch

**User Request:** "Find PRs targeting main branch"

**Expected Criteria:**
- Base filter: `--base main` OR `-B main`
- Valid branch name

**Platform:** All

---

## Test 7: Head Branch Filtering

**Description:** Find PRs from specific branch

**User Request:** "Find PRs from feature-auth branch"

**Expected Criteria:**
- Head filter: `--head feature-auth` OR `-H feature-auth`
- Branch name

**Platform:** All

---

## Test 8: Exclude Labels

**Description:** Exclude PRs with specific labels

**User Request:** "Find PRs NOT labeled as WIP"

**Expected Criteria:**
- Uses `--` flag before query
- Query includes `-label:wip`
- Entire query quoted
- Format: `gh search prs -- "query -label:wip"`

**Platform:** Unix/Linux/Mac

---

## Test 9: Author and State

**Description:** Find your open PRs

**User Request:** "Find my open pull requests"

**Expected Criteria:**
- Author: `--author @me`
- State: `--state open`
- Uses `@me` special value

**Platform:** All

---

## Test 10: Multiple Exclusions

**Description:** Exclude multiple labels

**User Request:** "Find PRs NOT labeled as draft or wip"

**Expected Criteria:**
- Uses `--` flag
- Query includes `-label:draft -label:wip`
- Multiple exclusions
- Properly quoted

**Platform:** Unix/Linux/Mac

---

## Test 11: Reviewed By User

**Description:** Find PRs reviewed by specific user

**User Request:** "Find PRs reviewed by octocat"

**Expected Criteria:**
- Reviewed by: `--reviewed-by octocat`
- No @ prefix on username
- Only @ for @me

**Platform:** All

---

## Test 12: Comment Count

**Description:** Filter by comment activity

**User Request:** "Find highly discussed PRs with over 20 comments"

**Expected Criteria:**
- Comments filter: `--comments ">20"`
- Comparison operator quoted
- NOT unquoted `>20`

**Platform:** All

---

## Test 13: Search in Title

**Description:** Search only in PR titles

**User Request:** "Find PRs with security in the title"

**Expected Criteria:**
- Query: `"security in:title"` OR
- Match filter: `--match title`
- Limits search to title field

**Platform:** All

---

## Test 14: Multi-word Label

**Description:** Label with spaces needs inner quotes

**User Request:** "Find PRs labeled as 'needs review'"

**Expected Criteria:**
- Label syntax: `label:"needs review"`
- Inner quotes around "needs review"
- May need outer quotes for entire query

**Platform:** All

---

## Test 15: PowerShell Exclusion

**Description:** PowerShell requires `--%` for exclusions

**User Request:** "On PowerShell, find PRs NOT labeled as draft"

**Expected Criteria:**
- Command starts with `gh --%`
- Includes `--` before query
- Query contains `-label:draft`
- Format: `gh --% search prs -- "-label:draft"`

**Platform:** PowerShell
