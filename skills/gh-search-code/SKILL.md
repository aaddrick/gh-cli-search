---
name: gh-search-code
description: Use when searching code within GitHub repositories - provides syntax for file extensions, filenames, languages, sizes, exclusions, and using -w flag for regex search via web interface
---

# GitHub CLI: Search Code

## Overview

Search for code within GitHub repositories using `gh search code`. **Important**: CLI API uses legacy search engine. For regex and advanced features, use `-w` flag to open in web browser.

## When to Use

Use this skill when:
- Searching for code patterns across repositories
- Finding specific file types or filenames
- Locating code by language or file size
- Need to exclude certain results (requires `--` flag)
- **Need regex search** (use `-w` to open in browser)

## Syntax

```bash
gh search code <query> [flags]
```

## Key Flags Reference

| Flag | Purpose | Example |
|------|---------|---------|
| `--extension <string>` | Filter by file extension | `--extension js` |
| `--filename <string>` | Target specific filenames | `--filename package.json` |
| `--language <string>` | Filter by programming language | `--language python` |
| `--owner <strings>` | Limit to specific owners | `--owner microsoft` |
| `-R, --repo <strings>` | Search within repository | `--repo cli/cli` |
| `--size <string>` | Filter by file size (KB) | `--size ">100"` |
| `--match <strings>` | Search in file or path | `--match file` or `--match path` |
| `-L, --limit <int>` | Max results (default: 30) | `--limit 100` |
| `-w, --web` | Open in browser | `-w` |
| `--json <fields>` | JSON output | `--json path,repository` |

## JSON Output Fields

Available fields: `path`, `repository`, `sha`, `textMatches`, `url`

## Critical Syntax Rules

### 1. Exclusions Require `--`

**Unix/Linux/Mac:**
```bash
gh search code -- "function -filename:test.js"
```

**PowerShell:**
```powershell
gh --% search code -- "function -filename:test.js"
```

### 2. Quoting Rules

**Multi-word search:**
```bash
gh search code "error handling"
```

**Complex queries with qualifiers:**
```bash
gh search code "TODO in:file" --language javascript
```

### 3. Size Comparisons

Use quotes for comparison operators:
```bash
gh search code "import" --size ">50" --language python
```

## Common Use Cases

**Search for function patterns:**
```bash
gh search code "async function" --language typescript
```

**Find configuration files:**
```bash
gh search code "database" --filename config.json --owner myorg
```

**Search in specific repo:**
```bash
gh search code "TODO" --repo owner/repo --language go
```

**Exclude test files:**
```bash
gh search code -- "function -filename:test"
```

**Search by file size:**
```bash
gh search code "import" --size "100..500" --language python
```

**Use regex (via web):**
```bash
# Open in browser for regex support
gh search code "function.*test" --language javascript -w
# Web UI allows: /function.*test/ or /class\s+\w+/
```

**Build complex query, refine in web:**
```bash
# Start with CLI filters, finish with regex in browser
gh search code --owner microsoft --language typescript -w
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| `gh search code import -language:js` | `-language` interpreted as flag | Use `--`: `gh search code -- "import -language:js"` |
| Not quoting multi-word queries | Searches separately | Quote: `"error handling"` |
| Forgetting quotes on comparisons | Shell interprets `>` | Quote: `--size ">100"` |
| Using `-filename` inline without `--` | Parsed as flag | Use `--`: `-- "code -filename:test"` |
| Trying regex via CLI | CLI API doesn't support regex | Use `-w` flag: `gh search code "pattern" -w` |

## Installation Check

If `gh` command not found:
```bash
# Check if gh is installed
which gh

# If not installed, see: https://cli.github.com/manual/installation
```

If not authenticated:
```bash
# Authenticate with GitHub
gh auth login
```

## Web Browser Flag (`-w/--web`)

**Important workaround for advanced features:**

The `-w/--web` flag opens your search in GitHub's web interface, which supports features not available via CLI API:

### Regex Search (Web Only)

```bash
# This opens in browser where you can use regex
gh search code "function.*test" --language javascript -w

# In the web UI, you can then modify to use regex syntax:
# /function.*test/ language:javascript
```

### When to Use `-w`

Use the web flag when you need:
- **Regex patterns** - `/pattern/` syntax for complex matching
- **Advanced filters** - Newer GitHub search features
- **Visual browsing** - Easier to explore results visually
- **Better results** - Web uses newer search engine

### Combining CLI + Web

```bash
# Build query with CLI, open in web for regex
gh search code --language python --repo myorg/myrepo -w
# Then add regex pattern in web UI
```

## Limitations (CLI API)

- Powered by legacy GitHub search engine
- Results may differ from github.com
- **Regex search not available via CLI** (use `-w` flag instead)
- Some advanced features may not work
- **Workaround:** Use `-w/--web` to access full GitHub search features

## Related

- GitHub search syntax: https://docs.github.com/search-github/searching-on-github/searching-code
- For searching other resources: `gh-search-issues`, `gh-search-prs`, `gh-search-repos`, `gh-search-commits`
