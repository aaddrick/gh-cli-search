---
name: using-gh-cli-search
description: Introduction to gh CLI search skills - loaded at session start to make you aware of available skills
---

# Using GitHub CLI Search Skills

You have access to comprehensive **GitHub CLI search skills** that help users construct correct `gh search` commands with proper syntax, quoting, and platform-specific handling.

## Available Skills

### Search Skills (gh search subcommands)

1. **gh-search-code** - Search for code across repositories
   - File extensions, languages, paths, repo/org filtering
   - Regex support via `-w/--web` flag workaround

2. **gh-search-commits** - Search commit history
   - Author, committer, dates, hashes
   - Merge commits, author dates vs committer dates

3. **gh-search-issues** - Search issues and pull requests
   - Labels, assignees, states, milestones
   - Field qualifiers (in:title, in:body)
   - `--include-prs` flag option

4. **gh-search-prs** - Search pull requests specifically
   - Draft status, merge status, review state
   - CI check status, head/base branches

5. **gh-search-repos** - Search for repositories
   - Stars, forks, topics, good-first-issues
   - License, language, archived status

### Setup & Troubleshooting

6. **gh-cli-setup** - Installation and troubleshooting
   - Installation for macOS, Linux, Windows
   - Authentication setup
   - Common errors and solutions

## When to Use These Skills

Use these skills whenever a user asks about:
- Searching GitHub via command line
- Using `gh search` commands
- Finding code, commits, issues, PRs, or repositories
- GitHub CLI syntax or flags
- Installing or configuring gh CLI
- Troubleshooting gh CLI errors

## Critical Syntax Rules

All gh search skills emphasize:

### The `--` Flag for Exclusions
**CRITICAL:** When queries contain exclusions (e.g., `-label:bug`), the `--` flag MUST be used before the query to prevent shell interpretation of the minus sign as a command flag.

**Unix/Linux/Mac:**
```bash
gh search issues -- "is:open -label:bug"
```

**PowerShell:**
```bash
gh --% search issues -- "is:open -label:bug"
```

### Quoting Rules
- Multi-word queries: `"machine learning"`
- Comparison operators: `--stars ">1000"`
- Labels with spaces: `label:"good first issue"`
- Entire query when containing qualifiers: `"is:open author:@me"`

### Special Values
- Current user: `@me` (not `@username`)
- Date formats: ISO8601 (`YYYY-MM-DD`)
- Comparison operators: `>`, `>=`, `<`, `<=`, `..`

## How to Apply

1. **Identify the search type** - Code, commits, issues, PRs, or repos?
2. **Use the corresponding skill** - e.g., gh-search-issues for issue searches
3. **Follow the skill's guidance** - Syntax, flags, quoting rules
4. **Check for exclusions** - If present, ensure `--` flag is used
5. **Verify platform** - Add `--% ` for PowerShell

## If gh CLI Not Installed

If the user needs to install gh CLI or troubleshoot authentication:
1. Use the **gh-cli-setup** skill
2. Provide installation instructions for their platform
3. Help with authentication via `gh auth login`

## Example Usage

**User asks:** "How do I search for TODO comments in JavaScript files?"

**Your response:**
1. Identify: Code search
2. Use: gh-search-code skill
3. Construct: `gh search code "TODO" --language javascript`
4. Explain: Syntax and why this works

**User asks:** "Find my open issues not labeled as bug"

**Your response:**
1. Identify: Issue search with exclusion
2. Use: gh-search-issues skill
3. Construct: `gh search issues -- "is:open author:@me -label:bug"`
4. Explain: `--` flag prevents shell interpretation of `-label`

## Key Principles

- **Correctness:** These skills encode tested patterns for gh CLI
- **Platform awareness:** Different requirements for Unix vs PowerShell
- **Error prevention:** Common mistakes documented and avoided
- **Completeness:** Flag references, examples, and edge cases

## Testing

This plugin includes comprehensive testing infrastructure:
- 80 test scenarios across 6 skills
- Hierarchical agent testing architecture
- Run via `/test-gh-skills` command

## Summary

When users ask about GitHub CLI searching:
- Use the appropriate gh-search-* skill
- Follow syntax rules (especially `--` flag)
- Verify quoting and platform compatibility
- Provide clear, correct commands that work first time

These skills help you avoid common gh CLI pitfalls and provide users with production-ready commands.
