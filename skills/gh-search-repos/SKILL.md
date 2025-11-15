---
name: gh-search-repos
description: Use when searching GitHub repositories - provides syntax for filtering by stars, forks, language, topics, license, archived status, and all repository attributes
---

# GitHub CLI: Search Repositories

## Overview

Search for repositories on GitHub using `gh search repos`. Filter by stars, forks, language, topics, license, and more.

## When to Use

Use this skill when:
- Finding repositories by popularity (stars/forks)
- Searching by programming language or topics
- Finding repos with good first issues
- Filtering by license or archived status
- Need to exclude certain results (requires `--` flag)

## Syntax

```bash
gh search repos [<query>] [flags]
```

## Key Flags Reference

### Repository Attributes

| Flag | Purpose | Example |
|------|---------|---------|
| `--language <string>` | Programming language | `--language python` |
| `--topic <strings>` | Repository topics | `--topic machine-learning` |
| `--license <strings>` | License type | `--license mit` |
| `--archived {true\|false}` | Archived state | `--archived false` |
| `--owner <strings>` | Repository owner | `--owner github` |
| `--visibility <string>` | Visibility: public, private, internal | `--visibility public` |

### Popularity Metrics

| Flag | Purpose | Example |
|------|---------|---------|
| `--stars <number>` | Star count | `--stars ">1000"` |
| `--forks <number>` | Fork count | `--forks ">100"` |
| `--followers <number>` | Follower count | `--followers ">50"` |
| `--size <string>` | Size in KB | `--size "100..1000"` |

### Issue Counts

| Flag | Purpose | Example |
|------|---------|---------|
| `--good-first-issues <number>` | "Good first issue" label count | `--good-first-issues ">=5"` |
| `--help-wanted-issues <number>` | "Help wanted" label count | `--help-wanted-issues ">=3"` |

### Date Filters

| Flag | Purpose | Example |
|------|---------|---------|
| `--created <date>` | Creation date | `--created ">2024-01-01"` |
| `--updated <date>` | Last update date | `--updated ">2024-06-01"` |

### Search Scope

| Flag | Purpose | Example |
|------|---------|---------|
| `--match <strings>` | Search in: name, description, readme | `--match name` |
| `--include-forks {false\|true\|only}` | Include/exclude forks | `--include-forks false` |

### Output & Sorting

| Flag | Purpose | Example |
|------|---------|---------|
| `-L, --limit <int>` | Max results (default: 30) | `--limit 100` |
| `--sort <string>` | Sort by: stars, forks, updated, etc. | `--sort stars` |
| `--order <string>` | Sort direction: asc or desc | `--order desc` |
| `--json <fields>` | JSON output | `--json name,stargazersCount,language` |
| `-w, --web` | Open in browser | `-w` |

## JSON Output Fields

`createdAt`, `defaultBranch`, `description`, `forksCount`, `fullName`, `hasDownloads`, `hasIssues`, `hasPages`, `hasProjects`, `hasWiki`, `homepage`, `id`, `isArchived`, `isDisabled`, `isFork`, `isPrivate`, `language`, `license`, `name`, `openIssuesCount`, `owner`, `pushedAt`, `size`, `stargazersCount`, `updatedAt`, `url`, `visibility`, `watchersCount`

## Critical Syntax Rules

### 1. Exclusions Require `--`

**Unix/Linux/Mac:**
```bash
gh search repos -- "cli -language:javascript"
```

**PowerShell:**
```powershell
gh --% search repos -- "cli -language:javascript"
```

### 2. Special Values

- Multiple topics: `--topic unix,terminal`
- Boolean flags: `--archived false` or `--archived true`
- Fork inclusion: `--include-forks false|true|only`

### 3. Quoting Rules

**Multi-word search:**
```bash
gh search repos "machine learning"
```

**Comparison operators need quotes:**
```bash
gh search repos "python" --stars ">1000"
```

**Ranges use quotes:**
```bash
gh search repos "cli" --stars "100..500"
```

## Common Use Cases

**Find popular Python repos:**
```bash
gh search repos "data science" --language python --stars ">5000"
```

**Find repos with good first issues:**
```bash
gh search repos --language javascript --good-first-issues ">=10"
```

**Find recently updated repos:**
```bash
gh search repos "react" --updated ">2024-01-01" --stars ">100"
```

**Find repos by topic:**
```bash
gh search repos --topic machine-learning --language python
```

**Find repos by license:**
```bash
gh search repos "web framework" --license mit,apache-2.0
```

**Exclude archived repos:**
```bash
gh search repos "cli tool" --archived false
```

**Find repos by organization:**
```bash
gh search repos --owner microsoft --visibility public
```

**Exclude forks:**
```bash
gh search repos "starter" --include-forks false
```

**Find only forks:**
```bash
gh search repos "template" --include-forks only
```

**Find repos in star range:**
```bash
gh search repos "game engine" --stars "100..1000"
```

**Exclude specific language:**
```bash
gh search repos -- "cli -language:go"
```

**Search in name only:**
```bash
gh search repos "awesome" --match name
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| `gh search repos cli -language:js` | `-language` interpreted as flag | Use `--`: `-- "cli -language:js"` |
| Not quoting comparisons | Shell interprets `>` | Quote: `--stars ">1000"` |
| `--archived archived` | Invalid value | Use boolean: `--archived true` or `false` |
| Not quoting multi-word search | Searches separately | Quote: `"machine learning"` |
| Using `@` with owner | Invalid syntax | Drop `@`: `--owner github` |
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
- `..` - Range: `100..1000` or `2024-01-01..2024-12-31`

## Common Licenses

- `mit` - MIT License
- `apache-2.0` - Apache License 2.0
- `gpl-3.0` - GNU GPL v3
- `bsd-2-clause` - BSD 2-Clause
- `bsd-3-clause` - BSD 3-Clause
- `mpl-2.0` - Mozilla Public License 2.0
- `isc` - ISC License

## Match Field Options

- `name` - Search repository names only
- `description` - Search descriptions only
- `readme` - Search README files only

Example: `gh search repos "documentation" --match readme`

## Related

- GitHub search syntax: https://docs.github.com/search-github/searching-on-github/searching-for-repositories
- For searching other resources: `gh-search-code`, `gh-search-commits`, `gh-search-issues`, `gh-search-prs`
