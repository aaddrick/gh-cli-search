# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

 - This section intentionally left blank

## [1.0.0] - 2025-11-15

### Added

- Initial public release of GitHub CLI Search plugin for Claude Code
- Nine comprehensive skills for GitHub CLI search functionality:
  - `gh-search-code` - Search code by file extension, language, path, content, and size
  - `gh-search-commits` - Search commit history by author, date range, hash, and message
  - `gh-search-issues` - Search issues by label, state, assignee, author, and dates
  - `gh-search-prs` - Search pull requests by status, reviews, CI checks, and branches
  - `gh-search-repos` - Search repositories by stars, forks, language, topics, and licenses
  - `gh-cli-setup` - Installation and troubleshooting guide for GitHub CLI
  - `gh-search` - General reference for syntax rules across all search types
  - `testing-gh-skills` - Orchestrates comprehensive test suite execution via hierarchical agent architecture
  - `using-gh-cli-search` - Introduction skill loaded at session start for skill awareness
- Six slash commands for quick skill invocation and testing:
  - `/gh-search-code`
  - `/gh-search-commits`
  - `/gh-search-issues`
  - `/gh-search-prs`
  - `/gh-search-repos`
  - `/test-gh-skills` - Executes full test suite
- Three-tier hierarchical testing agent architecture:
  - `test-orchestrator` - Manages overall test execution and generates master report
  - `test-group-leader` - Coordinates tests within scenario files and generates group reports
  - `test-validator` - Executes individual tests and validates responses against criteria
- Session-start hook system with automatic skill loading:
  - `hooks/hooks.json` - Hook configuration following Claude Code plugin hooks specification
  - `hooks/session-start.sh` - Shell script that loads `using-gh-cli-search` skill at session initialization
- Complete plugin structure following Claude Code plugin specification:
  - `.claude-plugin/plugin.json` - Plugin manifest
  - `.claude-plugin/marketplace.json` - Marketplace catalog
- Comprehensive test infrastructure with 80 test scenarios:
  - 6 test scenario files in `testing/scenarios/`
  - `testing/scripts/run-single-test.sh` - Script for executing individual tests
  - `testing/README.md` - Complete testing documentation
  - Validates syntax, quoting, exclusions, special values, and platform-specific requirements
- Platform-specific handling for Unix/Linux/Mac and PowerShell environments
- Critical syntax guidance including:
  - `--` flag requirement for exclusions on Unix-based systems
  - `--%` requirement for PowerShell environments
  - Proper quoting rules for multi-word queries
  - `@me` special value for current user
  - ISO8601 date format support with comparison operators
- Installation support for multiple methods (marketplace, direct clone, manual, team configuration)
- Documentation with examples, common mistakes reference, and best practices
