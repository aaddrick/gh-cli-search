---
name: gh-search-issues
description: Use when searching GitHub issues - provides syntax for filtering by labels, state, assignees, authors, comments, reactions, dates, and includes option to search pull requests
---

# GitHub CLI: Search Issues

## Overview

Search for issues on GitHub using `gh search issues`. Add `--include-prs` flag to also search pull requests.

## When to Use

Use this skill when:
- Finding issues by label, state, or assignee
- Searching for issues by author or mentioned user
- Filtering by comment/reaction counts
- Finding issues by date ranges
- Need to include PRs in search (use `--include-prs`)
- Need to exclude certain results (requires `--` flag)

## Syntax

```bash
gh search issues [<query>] [flags]
```

## Key Flags Reference

### User Filters

| Flag | Purpose | Example |
|------|---------|---------|
| `--author <string>` | Created by user | `--author octocat` |
| `--assignee <string>` | Assigned to user | `--assignee @me` |
| `--mentions <user>` | Mentions specific user | `--mentions octocat` |
| `--commenter <user>` | Commented by user | `--commenter octocat` |
| `--team-mentions <string>` | Mentions team | `--team-mentions myteam` |

### Issue Attributes

| Flag | Purpose | Example |
|------|---------|---------|
| `--label <strings>` | Has specific labels | `--label bug,urgent` |
| `--state <string>` | Issue state: open or closed | `--state open` |
| `--milestone <title>` | In specific milestone | `--milestone v1.0` |
| `--locked` | Locked conversation | `--locked` |
| `--no-label` | Has no labels | `--no-label` |

### Repository Filters

| Flag | Purpose | Example |
|------|---------|---------|
| `--owner <strings>` | Repository owner | `--owner github` |
| `-R, --repo <strings>` | Specific repository | `--repo cli/cli` |
| `--language <string>` | Repository language | `--language go` |
| `--visibility <strings>` | Repo visibility | `--visibility public` |
| `--archived` | In archived repos | `--archived` |

### Engagement Metrics

| Flag | Purpose | Example |
|------|---------|---------|
| `--comments <number>` | Number of comments | `--comments ">10"` |
| `--reactions <number>` | Reaction count | `--reactions ">5"` |
| `--interactions <number>` | Comments + reactions | `--interactions ">20"` |

### Date Filters

| Flag | Purpose | Example |
|------|---------|---------|
| `--created <date>` | Creation date | `--created ">2024-01-01"` |
| `--updated <date>` | Last update date | `--updated ">2024-06-01"` |
| `--closed <date>` | Close date | `--closed "<2024-12-31"` |

### Search Scope

| Flag | Purpose | Example |
|------|---------|---------|
| `--match <strings>` | Search in: title, body, comments | `--match title` |
| `--include-prs` | Include pull requests | `--include-prs` |

### Output & Sorting

| Flag | Purpose | Example |
|------|---------|---------|
| `-L, --limit <int>` | Max results (default: 30) | `--limit 100` |
| `--sort <string>` | Sort by: comments, created, reactions, etc. | `--sort comments` |
| `--order <string>` | Sort direction: asc or desc | `--order desc` |
| `--json <fields>` | JSON output | `--json number,title,state` |
| `-w, --web` | Open in browser | `-w` |

## JSON Output Fields

`assignees`, `author`, `authorAssociation`, `body`, `closedAt`, `commentsCount`, `createdAt`, `id`, `isLocked`, `isPullRequest`, `labels`, `number`, `repository`, `state`, `title`, `updatedAt`, `url`

## Critical Syntax Rules

### 1. Exclusions Require `--`

**Unix/Linux/Mac:**
```bash
gh search issues -- "bug -label:duplicate"
```

**PowerShell:**
```powershell
gh --% search issues -- "bug -label:duplicate"
```

### 2. Special Values

- `@me` - Current authenticated user
  ```bash
  gh search issues --assignee @me --state open
  ```

### 3. Quoting Rules

**Multi-word search:**
```bash
gh search issues "memory leak"
```

**Labels with spaces:**
```bash
gh search issues -- 'crash label:"bug fix"'
```

**Comparison operators need quotes:**
```bash
gh search issues "performance" --comments ">10"
```

## Common Use Cases

**Find your open issues:**
```bash
gh search issues --author @me --state open
```

**Find unassigned bugs:**
```bash
gh search issues --label bug --no-assignee --state open
```

**Find highly discussed issues:**
```bash
gh search issues --comments ">50" --state open --repo owner/repo
```

**Find stale issues:**
```bash
gh search issues --state open --updated "<2023-01-01"
```

**Search issues AND PRs:**
```bash
gh search issues "authentication" --include-prs --state open
```

**Exclude specific labels:**
```bash
gh search issues -- "crash -label:duplicate -label:wontfix"
```

**Find issues in milestone:**
```bash
gh search issues --milestone v2.0 --state open
```

**Find issues by title only:**
```bash
gh search issues "error in:title" --state open
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| `gh search issues bug -label:duplicate` | `-label` interpreted as flag | Use `--`: `-- "bug -label:duplicate"` |
| `--assignee @username` | Invalid `@` prefix | Use `@me` or drop `@`: `--assignee username` |
| Not quoting comparisons | Shell interprets `>` | Quote: `--comments ">10"` |
| `label:"bug fix"` outside quotes | Shell parsing error | Quote query: `'label:"bug fix"'` |
| Forgetting `--include-prs` | Misses pull requests | Add: `--include-prs` |
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

## Comparison Operators

- `>` - Greater than
- `>=` - Greater than or equal
- `<` - Less than
- `<=` - Less than or equal
- `..` - Range: `10..50` or `2024-01-01..2024-12-31`

## Field Qualifiers

Use `in:` to search specific fields:
- `in:title` - Search in title only
- `in:body` - Search in body only
- `in:comments` - Search in comments only

Example: `gh search issues "crash in:title" --state open`

## Related

- GitHub search syntax: https://docs.github.com/search-github/searching-on-github/searching-issues-and-pull-requests
- For searching other resources: `gh-search-code`, `gh-search-commits`, `gh-search-prs`, `gh-search-repos`
