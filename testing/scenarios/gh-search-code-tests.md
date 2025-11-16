# gh-search-code Test Scenarios

## Test 1: Basic Code Search

**Description:** Simple keyword search for code

**User Request:** "Search for TODO comments in JavaScript files across GitHub"

**Expected Criteria:**
- Command uses `gh search code`
- Query is `"TODO"`
- Language filter uses `--language javascript`
- Proper quoting

**Platform:** All

---

## Test 2: Extension Filtering

**Description:** Search by file extension

**User Request:** "Find code with 'import' in .ts files across repos"

**Expected Criteria:**
- Command uses `gh search code`
- Query is `"import"`
- Extension filter uses `--extension ts`
- No quotes around extension value

**Platform:** All

---

## Test 3: Exclusion with `--` Flag

**Description:** Exclude files using `--` flag

**User Request:** "Search for functions but NOT in test files across GitHub"

**User Request:** "Search for functions but NOT in test files across GitHub"

**Expected Criteria:**
- Command includes `--` before query
- Query contains `-filename:test`
- Entire query is quoted
- Format: `gh search code -- "function -filename:test"`

**Platform:** Unix/Linux/Mac

---

## Test 4: PowerShell Exclusion

**Description:** Exclusion on PowerShell requires `--%`

**User Request:** "On PowerShell, search for class definitions but NOT in test files across repos"

**Expected Criteria:**
- Command starts with `gh --%`
- Includes `--` before query
- Query contains `-filename:test`
- Format: `gh --% search code -- "class -filename:test"`

**Platform:** PowerShell

---

## Test 5: Multi-word Query

**Description:** Multi-word searches must be quoted

**User Request:** "Search for 'error handling' in Python code across repositories"

**Expected Criteria:**
- Query is quoted: `"error handling"`
- Language filter: `--language python`
- Not split into separate words

**Platform:** All

---

## Test 6: Owner Filtering

**Description:** Search within specific owner's repositories

**User Request:** "Find database config in kubernetes organization repositories"

**Expected Criteria:**
- Query includes search term
- Owner filter: `--owner myorg`
- No `@` prefix on owner name

**Platform:** All

---

## Test 7: Repository Scoping

**Description:** Search within specific repository

**User Request:** "Search for panic in the cli/cli repository"

**Expected Criteria:**
- Query is `"panic"`
- Repository filter: `-R cli/cli` or `--repo cli/cli` (both equivalent)
- Accepts either short or long form

**Platform:** All

---

## Test 8: File Size Filtering

**Description:** Filter by file size with comparison operators

**User Request:** "Find imports in Python files larger than 100KB across GitHub"

**Expected Criteria:**
- Query is `"import"`
- Language: `--language python`
- Size filter with quotes: `--size ">100"`
- Comparison operator quoted

**Platform:** All

---

## Test 9: Size Range

**Description:** Filter by file size range

**User Request:** "Search for TODO in files between 50 and 200 KB across repos"

**Expected Criteria:**
- Query is `"TODO"`
- Size range with quotes: `--size "50..200"`
- Range syntax uses `..`

**Platform:** All

---

## Test 10: Filename Filtering

**Description:** Search in specific filename

**User Request:** "Find database config in package.json files across GitHub"

**Expected Criteria:**
- Query is `"database"`
- Filename filter: `--filename package.json`
- Filename value may or may not be quoted

**Platform:** All

---

## Test 11: Web Flag for Regex

**Description:** Use web flag when regex is needed

**User Request:** "I need to use regex patterns to search for code in JavaScript (opening in browser is fine)"

**Expected Criteria:**
- Command includes `-w` or `--web` flag
- Query can be approximate (user will refine in web UI)
- Language filter: `--language javascript`
- Mentions that regex syntax available in web UI

**Platform:** All

---

## Test 12: Complex Query with Multiple Filters

**Description:** Combine multiple filters

**User Request:** "Search for authentication code in TypeScript files in microsoft org, excluding test files"

**Expected Criteria:**
- Uses `--` flag for exclusion
- Query includes `-filename:test`
- Language: `--language typescript`
- Owner: `--owner microsoft`
- Proper quoting of entire query

**Platform:** Unix/Linux/Mac

---

## Test 13: Match Field Qualifier

**Description:** Search in file contents vs path

**User Request:** "Search for config only in file contents, not paths, across GitHub"

**Expected Criteria:**
- Query is `"config"`
- Match filter: `--match file`
- Or inline qualifier: `"config in:file"`

**Platform:** All

---

## Test 14: Unquoted Comparison Operator Error Prevention

**Description:** Comparison operators must be quoted

**User Request:** "Find large files over 500KB across repositories"

**Expected Criteria:**
- Size filter properly quoted: `--size ">500"`
- NOT: `--size >500` (shell redirection)
- Quotes prevent shell interpretation

**Platform:** All

---

## Test 15: JSON Output

**Description:** Request JSON output for parsing

**User Request:** "Search for imports across GitHub and output as JSON with path and repository fields"

**Expected Criteria:**
- Query is `"import"`
- JSON flag: `--json path,repository`
- Field list comma-separated

**Platform:** All
