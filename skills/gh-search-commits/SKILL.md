---
name: gh-search-commits
description: Use when searching commit history on GitHub - provides syntax for filtering by author, committer, dates, hashes, and merge commits with proper exclusion handling
---

# GitHub CLI: Search Commits

## Overview

Search for commits on GitHub using `gh search commits`. Filter by author, committer, dates, commit hashes, and more.

## When to Use

Use this skill when:
- Finding commits by author or committer
- Searching commit messages for keywords
- Filtering by commit dates or hashes
- Looking for merge commits
- Need to exclude certain results (requires `--` flag)

## Syntax

```bash
gh search commits [<query>] [flags]
```

## Key Flags Reference

### Author & Committer Filters

| Flag | Purpose | Example |
|------|---------|---------|
| `--author <string>` | Filter by author username | `--author octocat` |
| `--author-name <string>` | Filter by author name | `--author-name "John Doe"` |
| `--author-email <string>` | Filter by author email | `--author-email john@example.com` |
| `--author-date <date>` | Filter by authored date | `--author-date ">2024-01-01"` |
| `--committer <string>` | Filter by committer username | `--committer octocat` |
| `--committer-name <string>` | Filter by committer name | `--committer-name "Jane Doe"` |
| `--committer-email <string>` | Filter by committer email | `--committer-email jane@example.com` |
| `--committer-date <date>` | Filter by committed date | `--committer-date "<2024-06-01"` |

### Commit Attributes

| Flag | Purpose | Example |
|------|---------|---------|
| `--hash <string>` | Filter by commit hash | `--hash 8dd03144` |
| `--parent <string>` | Filter by parent hash | `--parent abc123` |
| `--tree <string>` | Filter by tree hash | `--tree def456` |
| `--merge` | Filter merge commits only | `--merge` |

### Repository Filters

| Flag | Purpose | Example |
|------|---------|---------|
| `--owner <strings>` | Filter by repo owner | `--owner github` |
| `-R, --repo <strings>` | Search in specific repo | `--repo cli/cli` |
| `--visibility <strings>` | Filter by visibility | `--visibility public` |

### Output & Sorting

| Flag | Purpose | Example |
|------|---------|---------|
| `-L, --limit <int>` | Max results (default: 30) | `--limit 100` |
| `--sort <string>` | Sort by author-date or committer-date | `--sort author-date` |
| `--order <string>` | Sort direction: asc or desc | `--order asc` |
| `--json <fields>` | JSON output | `--json sha,author,commit` |
| `-w, --web` | Open in browser | `-w` |

## JSON Output Fields

Available fields: `author`, `commit`, `committer`, `id`, `parents`, `repository`, `sha`, `url`

## Critical Syntax Rules

### 1. Exclusions Require `--`

**Unix/Linux/Mac:**
```bash
gh search commits -- "fix -author:dependabot"
```

**PowerShell:**
```powershell
gh --% search commits -- "fix -author:dependabot"
```

### 2. Date Formats

Use ISO8601 format (YYYY-MM-DD) with comparison operators:
```bash
gh search commits --author-date ">2024-01-01"
gh search commits --committer-date "2024-01-01..2024-12-31"
```

### 3. Quoting Rules

**Multi-word search:**
```bash
gh search commits "bug fix"
```

**Date comparisons need quotes:**
```bash
gh search commits "refactor" --author-date "<2024-06-01"
```

## Common Use Cases

**Find commits by author:**
```bash
gh search commits --author octocat --repo cli/cli
```

**Search commit messages:**
```bash
gh search commits "security fix" --repo myorg/myrepo
```

**Find commits in date range:**
```bash
gh search commits "refactor" --author-date "2024-01-01..2024-12-31"
```

**Find merge commits:**
```bash
gh search commits --merge --repo owner/repo
```

**Exclude bot commits:**
```bash
gh search commits -- "deployment -author:dependabot"
```

**Search by commit hash:**
```bash
gh search commits --hash 8dd03144
```

**Find commits by email:**
```bash
gh search commits --author-email user@example.com
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| `gh search commits fix -author:bot` | `-author` interpreted as flag | Use `--`: `-- "fix -author:bot"` |
| `--author-date 2024-01-01` without comparison | May not work as expected | Use: `--author-date ">2024-01-01"` |
| Not quoting date comparisons | Shell interprets operators | Quote: `"<2024-06-01"` |
| `--author @octocat` | Invalid `@` prefix | Drop `@`: `--author octocat` |
| PowerShell without `--%` | Breaks with exclusions | Add: `gh --%` |

## Installation Check

If `gh` command not found:
```bash
# Check if gh is installed
which gh

# Install: https://cli.github.com/manual/installation
```

If not authenticated:
```bash
# Authenticate with GitHub
gh auth login
```

## Date Comparison Operators

- `>` - After date
- `>=` - On or after date
- `<` - Before date
- `<=` - On or before date
- `..` - Date range: `2024-01-01..2024-12-31`

## Related

- GitHub search syntax: https://docs.github.com/search-github/searching-on-github/searching-commits
- For searching other resources: `gh-search-code`, `gh-search-issues`, `gh-search-prs`, `gh-search-repos`
