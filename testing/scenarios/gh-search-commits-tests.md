# gh-search-commits Test Scenarios

## Test 1: Author Filtering

**Description:** Find commits by author

**User Request:** "Find commits by octocat in cli/cli repo"

**Expected Criteria:**
- Author: `--author octocat`
- No @ prefix
- Repository: `--repo cli/cli`

**Platform:** All

---

## Test 2: Date Range

**Description:** Filter commits by date range

**User Request:** "Find commits from 2024"

**Expected Criteria:**
- Author date: `--author-date "2024-01-01..2024-12-31"`
- ISO8601 format
- Range with `..`
- Quoted

**Platform:** All

---

## Test 3: Commit Message Search

**Description:** Search commit messages

**User Request:** "Find commits mentioning 'bug fix' in microsoft/vscode repository"

**Expected Criteria:**
- Query quoted: `"bug fix"`
- Multi-word phrase

**Platform:** All

---

## Test 4: Exclude Author

**Description:** Exclude commits from specific author

**User Request:** "Find commits NOT from dependabot across repos"

**Expected Criteria:**
- Uses `--` flag
- Query includes `-author:dependabot`
- Format: `gh search commits -- "fix -author:dependabot"`

**Platform:** Unix/Linux/Mac

---

## Test 5: Merge Commits

**Description:** Find only merge commits

**User Request:** "Find merge commits in golang/go repository"

**Expected Criteria:**
- Merge filter: `--merge` flag OR query includes `merge:true` or keyword `merge` (both are valid)
- Repository scope: `--repo golang/go` OR query includes `repo:golang/go`

**Platform:** All

---

## Test 6: Commit Hash

**Description:** Search by commit hash

**User Request:** "Find commits with hash starting with 8dd03144"

**Expected Criteria:**
- Hash filter: `--hash 8dd03144`
- Partial hash accepted

**Platform:** All

---

## Test 7: Email Filtering

**Description:** Find commits by author email

**User Request:** "Find commits from noreply@github.com across GitHub"

**Expected Criteria:**
- Author email: `--author-email noreply@github.com`
- Email address

**Platform:** All

---

## Test 8: Date Comparison

**Description:** Find commits after specific date

**User Request:** "Find commits after January 1, 2024"

**Expected Criteria:**
- Author date: `--author-date ">2024-01-01"`
- Comparison operator
- ISO8601 format
- Quoted

**Platform:** All

---

## Test 9: PowerShell Exclusion

**Description:** Exclude on PowerShell

**User Request:** "On PowerShell, find deployment commits NOT from bots"

**Expected Criteria:**
- Command starts with `gh --%`
- Includes `--` before query
- Query contains `-author:bot`
- Format: `gh --% search commits -- "deployment -author:bot"`

**Platform:** PowerShell

---

## Test 10: Committer vs Author

**Description:** Filter by committer (not author)

**User Request:** "Find commits where octocat was the committer across GitHub"

**Expected Criteria:**
- Committer: `--committer octocat`
- NOT --author (different role)
- No @ prefix

**Platform:** All
