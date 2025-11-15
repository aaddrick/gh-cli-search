---
name: gh-search-prs
description: Use when searching GitHub pull requests - provides syntax for filtering by draft status, merge status, review state, CI checks, branches, and all standard PR attributes
---

# GitHub CLI: Search Pull Requests

## Overview

Search for pull requests on GitHub using `gh search prs`. Includes PR-specific filters like draft status, merge state, review status, and CI checks.

## When to Use

Use this skill when:
- Finding PRs by draft, merge, or review status
- Searching PRs by branch names (base or head)
- Filtering by CI check status
- Finding PRs by labels, state, or assignees
- Need to exclude certain results (requires `--` flag)

## Syntax

```bash
gh search prs [<query>] [flags]
```

## Key Flags Reference

### PR-Specific Filters

| Flag | Purpose | Example |
|------|---------|---------|
| `--draft` | Filter draft PRs | `--draft` |
| `--merged` | Filter merged PRs | `--merged` |
| `--merged-at <date>` | Merged at date | `--merged-at ">2024-01-01"` |
| `-B, --base <string>` | Base branch name | `--base main` |
| `-H, --head <string>` | Head branch name | `--head feature-auth` |
| `--review <string>` | Review status | `--review approved` |
| `--review-requested <user>` | Review requested from | `--review-requested @me` |
| `--reviewed-by <user>` | Reviewed by user | `--reviewed-by octocat` |
| `--checks <string>` | CI check status | `--checks success` |

### User Filters

| Flag | Purpose | Example |
|------|---------|---------|
| `--author <string>` | Created by user | `--author octocat` |
| `--assignee <string>` | Assigned to user | `--assignee @me` |
| `--mentions <user>` | Mentions specific user | `--mentions octocat` |
| `--commenter <user>` | Commented by user | `--commenter octocat` |
| `--team-mentions <string>` | Mentions team | `--team-mentions myteam` |

### PR Attributes

| Flag | Purpose | Example |
|------|---------|---------|
| `--label <strings>` | Has specific labels | `--label bug,urgent` |
| `--state <string>` | PR state: open or closed | `--state open` |
| `--milestone <title>` | In specific milestone | `--milestone v1.0` |
| `--locked` | Locked conversation | `--locked` |
| `--no-label` | Has no labels | `--no-label` |

### Repository Filters

| Flag | Purpose | Example |
|------|---------|---------|
| `--owner <strings>` | Repository owner | `--owner github` |
| `-R, --repo <strings>` | Specific repository | `--repo cli/cli` |
| `--language <string>` | Repository language | `--language typescript` |
| `--visibility <strings>` | Repo visibility | `--visibility public` |
| `--archived` | In archived repos | `--archived` |

### Engagement Metrics

| Flag | Purpose | Example |
|------|---------|---------|
| `--comments <number>` | Number of comments | `--comments ">5"` |
| `--reactions <number>` | Reaction count | `--reactions ">10"` |
| `--interactions <number>` | Comments + reactions | `--interactions ">15"` |

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

### Output & Sorting

| Flag | Purpose | Example |
|------|---------|---------|
| `-L, --limit <int>` | Max results (default: 30) | `--limit 100` |
| `--sort <string>` | Sort by: comments, created, reactions, etc. | `--sort updated` |
| `--order <string>` | Sort direction: asc or desc | `--order desc` |
| `--json <fields>` | JSON output | `--json number,title,state,isDraft` |
| `-w, --web` | Open in browser | `-w` |

## JSON Output Fields

`assignees`, `author`, `authorAssociation`, `body`, `closedAt`, `commentsCount`, `createdAt`, `id`, `isDraft`, `isLocked`, `isPullRequest`, `labels`, `number`, `repository`, `state`, `title`, `updatedAt`, `url`

## Critical Syntax Rules

### 1. Exclusions Require `--`

**Unix/Linux/Mac:**
```bash
gh search prs -- "security -label:duplicate"
```

**PowerShell:**
```powershell
gh --% search prs -- "security -label:duplicate"
```

### 2. Special Values

- `@me` - Current authenticated user
  ```bash
  gh search prs --review-requested @me --state open
  ```

### 3. Review Status Values

- `none` - No reviews
- `required` - Review required
- `approved` - Approved
- `changes_requested` - Changes requested

### 4. Check Status Values

- `pending` - Checks pending
- `success` - All checks passed
- `failure` - Checks failed

### 5. Quoting Rules

**Multi-word search:**
```bash
gh search prs "bug fix"
```

**Labels with spaces:**
```bash
gh search prs -- 'refactor label:"needs review"'
```

**Comparison operators need quotes:**
```bash
gh search prs "performance" --comments ">5"
```

## Common Use Cases

**Find your open PRs:**
```bash
gh search prs --author @me --state open
```

**Find PRs awaiting your review:**
```bash
gh search prs --review-requested @me --state open
```

**Find draft PRs:**
```bash
gh search prs --draft --repo owner/repo
```

**Find merged PRs in date range:**
```bash
gh search prs --merged --merged-at "2024-01-01..2024-12-31"
```

**Find PRs with failing checks:**
```bash
gh search prs --checks failure --state open
```

**Find approved PRs not yet merged:**
```bash
gh search prs --review approved --state open --repo owner/repo
```

**Find PRs by base branch:**
```bash
gh search prs --base main --state open
```

**Find PRs with specific head branch:**
```bash
gh search prs --head feature-* --state open
```

**Exclude specific labels:**
```bash
gh search prs -- "refactor -label:wip -label:draft"
```

**Find stale PRs:**
```bash
gh search prs --state open --updated "<2024-01-01"
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| `gh search prs fix -label:wip` | `-label` interpreted as flag | Use `--`: `-- "fix -label:wip"` |
| `--review-requested @username` | Invalid `@` prefix | Use `@me` or drop `@`: `--review-requested username` |
| Not quoting comparisons | Shell interprets `>` | Quote: `--comments ">5"` |
| `label:"needs review"` outside quotes | Shell parsing error | Quote query: `'label:"needs review"'` |
| Using `--merged` with `--state open` | Contradictory filters | Merged PRs are closed; remove `--state` |
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

Example: `gh search prs "authentication in:title" --state open`

## Related

- GitHub search syntax: https://docs.github.com/search-github/searching-on-github/searching-issues-and-pull-requests
- For searching other resources: `gh-search-code`, `gh-search-commits`, `gh-search-issues`, `gh-search-repos`
