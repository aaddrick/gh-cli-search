# gh-search-issues Test Scenarios

## Test 1: Basic Issue Search with Exclusion

**Description:** Find open issues without a specific label

**User Request:** "Find my open issues that are NOT labeled as bug"

**Expected Criteria:**
- Uses `--` flag before query
- Query contains `is:open`, `author:@me`, `-label:bug`
- Special value `@me` used correctly
- Exclusion `-label:bug` inside quotes
- Format: `gh search issues -- "is:open author:@me -label:bug"`

**Platform:** Unix/Linux/Mac

---

## Test 2: PowerShell Issue Search with Exclusion

**Description:** Exclusion on PowerShell requires `--%`

**User Request:** "On PowerShell, find issues NOT labeled as duplicate"

**Expected Criteria:**
- Command starts with `gh --%`
- Includes `--` before query
- Query contains `-label:duplicate`
- Format: `gh --% search issues -- "is:issue -label:duplicate"`

**Platform:** PowerShell

---

## Test 3: Using @me Special Value

**Description:** Current user syntax with @me

**User Request:** "Find issues assigned to me that are open"

**Expected Criteria:**
- Uses `--assignee @me` OR `assignee:@me` in query
- State filter for open issues
- NOT `@username` (@ only for @me)

**Platform:** All

---

## Test 4: Incorrect @username Prevention

**Description:** Should NOT use @ with specific username

**User Request:** "Find issues authored by octocat"

**Expected Criteria:**
- Uses `--author octocat` (no @)
- NOT `--author @octocat`
- @ is only for @me

**Platform:** All

---

## Test 5: Label with Spaces

**Description:** Labels containing spaces need inner quotes

**User Request:** "Find issues with 'bug fix' label"

**Expected Criteria:**
- Query contains `label:"bug fix"`
- Inner quotes around "bug fix"
- Outer quotes around entire query if using inline syntax

**Platform:** All

---

## Test 6: Multiple Labels

**Description:** Filter by multiple labels

**User Request:** "Find issues labeled as bug and urgent"

**Expected Criteria:**
- Uses `--label bug,urgent` OR
- Query with `label:bug label:urgent`
- Comma-separated for flag syntax

**Platform:** All

---

## Test 7: Comment Count Filtering

**Description:** Filter by number of comments with comparison

**User Request:** "Find highly discussed issues with more than 50 comments"

**Expected Criteria:**
- Comment filter with quotes: `--comments ">50"`
- Comparison operator quoted
- State may be open

**Platform:** All

---

## Test 8: Date Range Filtering

**Description:** Filter by creation date range

**User Request:** "Find issues created in 2024"

**Expected Criteria:**
- Date filter: `--created "2024-01-01..2024-12-31"`
- ISO8601 date format
- Range syntax with `..`
- Quotes around date range

**Platform:** All

---

## Test 9: Include Pull Requests

**Description:** Search both issues and PRs

**User Request:** "Search for authentication issues and pull requests"

**Expected Criteria:**
- Query includes `"authentication"`
- Includes `--include-prs` flag
- Without flag, only returns issues

**Platform:** All

---

## Test 10: Search in Title Only

**Description:** Restrict search to title field

**User Request:** "Find issues with crash in the title"

**Expected Criteria:**
- Query uses `"crash in:title"` OR
- Match filter: `--match title`
- Limits search to title field

**Platform:** All

---

## Test 11: Repository Filtering

**Description:** Search issues in specific repository

**User Request:** "Find open bugs in the cli/cli repository"

**Expected Criteria:**
- Query or flag includes repository scope
- Repository: `--repo cli/cli`
- Label or query for "bug"
- State: `--state open`

**Platform:** All

---

## Test 12: Assignee Filtering

**Description:** Find issues assigned to specific user

**User Request:** "Find issues assigned to octocat"

**Expected Criteria:**
- Assignee: `--assignee octocat`
- No @ prefix for specific username
- Only use @ for @me

**Platform:** All

---

## Test 13: No Assignee

**Description:** Find unassigned issues

**User Request:** "Find open issues that are unassigned"

**Expected Criteria:**
- Uses `--no-assignee` flag OR
- Query includes `no:assignee`
- State filter for open

**Platform:** All

---

## Test 14: Milestone Filtering

**Description:** Filter by milestone

**User Request:** "Find issues in the v2.0 milestone"

**Expected Criteria:**
- Milestone filter: `--milestone v2.0` OR
- Query includes `milestone:v2.0`

**Platform:** All

---

## Test 15: Multi-word Search Term

**Description:** Search term with spaces must be quoted

**User Request:** "Search for memory leak issues"

**Expected Criteria:**
- Query quoted: `"memory leak"`
- NOT: `memory leak` (unquoted)
- Searches exact phrase

**Platform:** All

---

## Test 16: Reactions Filtering

**Description:** Filter by reaction count

**User Request:** "Find popular issues with more than 10 reactions"

**Expected Criteria:**
- Reactions filter with quotes: `--reactions ">10"`
- Comparison operator quoted
- NOT unquoted: `>10`

**Platform:** All

---

## Test 17: Updated Date Filtering

**Description:** Find stale issues not updated recently

**User Request:** "Find open issues not updated since January 1, 2023"

**Expected Criteria:**
- Updated filter: `--updated "<2023-01-01"`
- ISO8601 date format
- Comparison operator quoted
- State filter for open

**Platform:** All

---

## Test 18: Exclude Multiple Labels

**Description:** Exclude multiple labels with exclusions

**User Request:** "Find issues NOT labeled as duplicate or wontfix"

**Expected Criteria:**
- Uses `--` flag for exclusions
- Query includes `-label:duplicate -label:wontfix`
- Multiple exclusions in query string
- Entire query quoted

**Platform:** Unix/Linux/Mac

---

## Test 19: Author and Mentions

**Description:** Combine author and mentions filters

**User Request:** "Find issues I authored that mention octocat"

**Expected Criteria:**
- Author: `--author @me` or `author:@me`
- Mentions: `--mentions octocat` or `mentions:octocat`
- No @ on specific username

**Platform:** All

---

## Test 20: JSON Output with Fields

**Description:** Request specific JSON fields

**User Request:** "Search for bugs and output JSON with number, title, and state"

**Expected Criteria:**
- Query or label filter for "bug"
- JSON flag: `--json number,title,state`
- Field list comma-separated, no spaces

**Platform:** All
