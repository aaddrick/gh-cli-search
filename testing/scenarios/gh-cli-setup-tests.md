# gh-cli-setup Test Scenarios

## Test 1: Installation Check Command

**Description:** Verify gh installation

**User Request:** "How do I check if gh is installed?"

**Expected Criteria:**
- Command: `which gh` (Unix/Mac) OR `where gh` (Windows)
- Alternative: `gh --version`
- Checks PATH for gh binary

**Platform:** All

---

## Test 2: Authentication Command

**Description:** Authenticate with GitHub

**User Request:** "What command do I run to authenticate gh CLI?"

**Expected Criteria:**
- Command: `gh auth login`
- Interactive authentication
- No token visible in command

**Platform:** All

---

## Test 3: Check Auth Status

**Description:** Verify authentication status

**User Request:** "What command checks if I'm authenticated with gh?"

**Expected Criteria:**
- Command: `gh auth status`
- Shows current authentication state
- Lists authenticated accounts

**Platform:** All

---

## Test 4: Installation via Homebrew

**Description:** Install gh on macOS

**User Request:** "How do I install gh on macOS?"

**Expected Criteria:**
- Mentions: `brew install gh`
- Homebrew as recommended method
- Other methods also acceptable (MacPorts, Conda)

**Platform:** macOS

---

## Test 5: Installation on Ubuntu

**Description:** Install gh on Ubuntu/Debian

**User Request:** "How do I install gh on Ubuntu?"

**Expected Criteria:**
- Mentions apt repository setup
- Command: `sudo apt install gh`
- Repository URL provided

**Platform:** Linux (Debian/Ubuntu)

---

## Test 6: Rate Limit Check

**Description:** Check API rate limit

**User Request:** "How do I check my GitHub API rate limit?"

**Expected Criteria:**
- Command: `gh api rate_limit`
- Shows remaining requests
- Authenticated vs unauthenticated limits

**Platform:** All

---

## Test 7: Configuration View

**Description:** View gh configuration

**User Request:** "How do I see my gh CLI configuration?"

**Expected Criteria:**
- Command: `gh config list`
- Shows all settings
- Config file location mentioned

**Platform:** All

---

## Test 8: Token Scope Error

**Description:** Diagnose insufficient permissions

**User Request:** "I'm getting HTTP 403 errors, what's wrong?"

**Expected Criteria:**
- Mentions insufficient token scopes
- Solution: re-authenticate with proper scopes
- Command: `gh auth login --scopes repo,read:org`

**Platform:** All

---

## Test 9: Network Error Diagnosis

**Description:** Handle network connectivity issues

**User Request:** "I can't connect to github.com. What commands should I run to diagnose the issue?"

**Expected Criteria:**
- Test connectivity: `ping github.com`
- Check DNS: `nslookup github.com`
- Proxy configuration if needed

**Platform:** All

---

## Test 10: Multiple Account Management

**Description:** Switch between GitHub accounts

**User Request:** "How do I use multiple GitHub accounts?"

**Expected Criteria:**
- Login to multiple hosts: `gh auth login --hostname`
- Switch accounts: `gh auth switch`
- Check active account: `gh auth status`

**Platform:** All
