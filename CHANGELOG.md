# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

 - This section intentionally left blank

## [1.1.0] - 2025-11-15

### Changed

- **BREAKING: Test infrastructure redesigned** - Replaced 3-tier agent hierarchy with Python orchestrator
  - Old: test-orchestrator → test-group-leader → test-validator (167 context loads)
  - New: `testing/scripts/run-all-tests.py` (80 context loads)
  - Performance improved from timeouts to ~6 seconds per test
  - Total suite execution: ~8 minutes for 80 tests
- Updated `testing-gh-skills` skill documentation to reflect Python orchestrator approach
- **`testing-gh-skills` now marked as SLASH COMMAND ONLY** - Never invokes automatically
  - Added critical warning section to prevent accidental expensive test runs
  - Only triggers via `/test-gh-skills` or explicit "run the test suite" requests
- Enhanced `using-gh-cli-search` skill with mandatory directive style
  - Stronger language to ensure skills are used when available
  - Better prevents agents from bypassing skill system

### Added

- **Python test orchestrator** (`testing/scripts/run-all-tests.py`)
  - Parses test scenarios from markdown files
  - Executes 80 tests sequentially with clean isolation
  - Generates 3-level reports (master, group, individual)
  - Tracks execution time and pass/fail statistics
  - Enhanced command extraction for setup commands (ping, nslookup, brew, apt)
  - Validates skill usage (gh search vs gh subcommands)
- **Test-reviewer agent** (`agents/test-reviewer.md`)
  - Post-test analysis agent for comprehensive result review
  - Identifies failure patterns across all tests
  - Performs root cause analysis (skill vs test vs agent vs infrastructure issues)
  - Creates REVIEWER-NOTES.md with prioritized recommendations
  - Integrated into testing workflow as optional step 3
- Execution timing metrics to test suite output
  - Start time, end time, total duration
  - Average time per test
  - Included in all reports
- Root `.gitignore` for Python, IDE, and OS files
- Test reports `.gitignore` to exclude generated reports from git

### Fixed

- **Critical permission mode bug** in `run-single-test.sh`
  - Changed from invalid `acceptAll` to `bypassPermissions`
  - Resolved 100% test failure rate issue
- Test timeout issues
  - Disabled episodic memory searches during tests (major speedup)
  - Increased timeout from 60s to 120s for complex tests
  - Added concise output mode to reduce response times
- Command extraction failures
  - Enhanced regex patterns for various command formats
  - Added support for setup/diagnostic commands
  - Better handling of inline vs code block commands
- Test prompts improved for clarity
  - "How do I authenticate" → "What command do I run to authenticate"
  - More explicit requests for command output in code blocks

### Improved

- Test pass rate: 70% → 73.8% (59/80 tests passing)
- Test execution speed: 60s+ timeouts → ~6s per test
- Timeout rate: 30% → 0%
- Skill tool invocation explicitly added to test runner
  - Ensures gh-cli-search skills are loaded during tests
  - Tests validate actual skill behavior, not generic responses

### Removed

- Five unused slash commands (`/gh-search-code`, `/gh-search-commits`, `/gh-search-issues`, `/gh-search-prs`, `/gh-search-repos`)
  - Skills can be invoked directly without dedicated slash commands
  - Kept `/test-gh-skills` as the only necessary slash command
- Redundant `.gitignore` in `testing/reports/` (moved to root)
- **Old 3-tier agent hierarchy** (`agents/test-orchestrator.md`, `agents/test-group-leader.md`, `agents/test-validator.md`)
  - Replaced by Python orchestrator + test-reviewer agent
  - Old architecture was token-heavy (167 context loads vs 80 now)

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
