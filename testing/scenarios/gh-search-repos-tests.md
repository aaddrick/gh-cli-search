# gh-search-repos Test Scenarios

## Test 1: Star Count Filtering

**Description:** Find popular repositories by stars

**User Request:** "Find Python repos with more than 1000 stars across GitHub"

**Expected Criteria:**
- Language: `--language python`
- Stars filter: `--stars ">1000"`
- Comparison operator quoted

**Platform:** All

---

## Test 2: Topic Filtering

**Description:** Search by repository topics

**User Request:** "Find repos tagged with machine-learning across GitHub"

**Expected Criteria:**
- Topic filter: `--topic machine-learning`
- Topic name

**Platform:** All

---

## Test 3: Multi-word Query

**Description:** Multi-word search must be quoted

**User Request:** "Search for 'web framework' repositories across GitHub"

**Expected Criteria:**
- Query quoted: `"web framework"`
- NOT unquoted (searches separately)

**Platform:** All

---

## Test 4: Exclude Archived

**Description:** Exclude archived repositories

**User Request:** "Find active CLI tools across GitHub, not archived"

**Expected Criteria:**
- Archived filter: `--archived false`
- Boolean value: true or false

**Platform:** All

---

## Test 5: Good First Issues

**Description:** Find repos with beginner-friendly issues

**User Request:** "Find JavaScript repos with at least 10 good first issues across GitHub"

**Expected Criteria:**
- Language: `--language javascript`
- Good first issues: `--good-first-issues ">=10"`
- Comparison with quotes

**Platform:** All

---

## Test 6: Fork Filtering

**Description:** Exclude forked repositories

**User Request:** "Find original projects across GitHub, not forks"

**Expected Criteria:**
- Include forks: `--include-forks false`
- Value: false, true, or only

**Platform:** All

---

## Test 7: Owner Filtering

**Description:** Search repositories by owner

**User Request:** "Search for CLI tool repositories with 1000+ stars across GitHub"

**Expected Criteria:**
- Owner: `--owner microsoft`
- No @ prefix
- Visibility: `--visibility public`

**Platform:** All

---

## Test 8: Star Range

**Description:** Filter by star count range

**User Request:** "Find repos with 100 to 500 stars across GitHub"

**Expected Criteria:**
- Stars range: `--stars "100..500"`
- Range with `..`
- Quoted

**Platform:** All

---

## Test 9: License Filtering

**Description:** Find repos by license

**User Request:** "Find MIT licensed Python projects across GitHub"

**Expected Criteria:**
- License: `--license mit`
- Language: `--language python`
- License identifier

**Platform:** All

---

## Test 10: Exclude Language

**Description:** Exclude specific programming language

**User Request:** "Find CLI tools NOT written in Go across GitHub"

**Expected Criteria:**
- Uses `--` flag
- Query includes `-language:go`
- Format: `gh search repos -- "cli -language:go"`

**Platform:** Unix/Linux/Mac
