# GitHub CLI Search Plugin

A Claude Code plugin providing skills and commands for using GitHub CLI (`gh`) search effectively with correct syntax, quoting, and platform-specific handling.

## What's Included

**Search Skills:**
- **gh-search-code** - Search code by file extension, language, path, content, size
- **gh-search-commits** - Search commits by author, date range, hash, message
- **gh-search-issues** - Search issues by label, state, assignee, author, dates
- **gh-search-prs** - Search PRs by draft/merge status, reviews, CI checks, branches
- **gh-search-repos** - Search repos by stars, forks, language, topics, licenses
- **gh-cli-setup** - Installation and troubleshooting for `gh` CLI
- **gh-search** - General reference for syntax rules across all search types

**Slash Commands:**
- `/gh-search-code`, `/gh-search-commits`, `/gh-search-issues`, `/gh-search-prs`, `/gh-search-repos`

**Session-Start Hook:** 
Automatically loads skill awareness at session start so Claude knows how to construct correct `gh` commands immediately.

## Installation

### Claude Code (via Plugin Marketplace)

```bash
/plugin marketplace add aaddrick/helpful-tools-marketplace
```
```bash
/plugin install gh-cli-search@helpful-tools-marketplace
```

### Verify Installation

Check that commands appear:

```bash
/help
```

```
# Should see:
# /gh-cli-search:gh-search-code - Search for code within GitHub repositories
# /gh-cli-search:gh-search-commits - Search commit history on GitHub
# /gh-cli-search:gh-search-issues - Search GitHub issues
# ...
```

## Examples

```bash
# Search popular Python ML repos
gh search repos "machine learning" --language python --stars ">1000"

# Find your open issues without bug label (note the -- flag!)
gh search issues -- "is:open author:@me -label:bug"

# Find PRs awaiting your review
gh search prs --review-requested @me --state open

# Search for TODO comments in your org's JavaScript code
gh search code "TODO" --owner myorg --language javascript

# Find commits by author in date range
gh search commits --author octocat --author-date "2024-01-01..2024-12-31"
```

## Critical Syntax Rules

- **Exclusions require `--` flag** on Unix/Linux/Mac: `gh search issues -- "-label:bug"`
- **PowerShell needs `--%`**: `gh --% search issues -- "query"`
- **Multi-word queries need quotes**: `"machine learning"` not `machine learning`
- **Use `@me` for current user**, not `@username`
- **Dates use ISO8601**: `2024-01-01..2024-12-31`

## Requirements

- GitHub CLI (`gh`) installed and authenticated
- GitHub account (public repos work without auth but with rate limits)

## Testing

Run the comprehensive test suite (80 test scenarios):

```bash
/test-gh-skills
```

See `testing/README.md` for details.

## Contributing

Test changes using TDD methodology, ensure cross-platform compatibility, update version in `plugin.json`. Follow the existing skill structure.

## Resources

- [GitHub CLI Manual](https://cli.github.com/manual/)
- [GitHub Search Syntax](https://docs.github.com/search-github/getting-started-with-searching-on-github/understanding-the-search-syntax)
- [Claude Code Plugin Docs](https://code.claude.com/docs)

## License

[MIT License](LICENSE)
