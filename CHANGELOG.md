# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

 - This section intentionally left blank

## [1.2.0] - 2025-11-15

### Added

- Product-manager agent for orchestrating automated test iteration loops with historical context tracking.
- Developer agent for implementing fixes autonomously between test iterations.
- Parallel test execution capability with automatic test-reviewer invocation.
- Cross-execution continuity system with sequential iteration numbering (testing/reports/YYYY-MM-DD_N/).
- testing/GUIDANCE.md for centralized decision-making reference across agents.
- Duration tracking throughout test execution (individual, group, and total suite timing).
- --verbose flag for run-all-tests.py to display real-time agent output.
- Commit ID tracking in agent notes and reports for tracing fixes across iterations.
- Post-fix validation and headless mode clarification in test runner.
- Comprehensive "Exclusion Syntax (Critical!)" sections to all search skills with platform-specific examples.

### Changed

- Test orchestrator refactored into modular package structure with 8 separate modules for improved maintainability.
- Test-reviewer agent completely rewritten following subagent best practices with better root cause analysis.
- All search skills updated to emphasize GitHub-wide scope rather than single repository searches.
- Test scenarios updated with explicit scope indicators and improved validation criteria.
- Agent autonomy improved to only halt for truly new decisions, not routine operations.
- Master REPORT.md enhanced to include full test details in Failed Tests Summary.
- Testing README comprehensively updated for current architecture.

### Fixed

- Test 9 validation issues with improved criteria.
- Test accuracy improvements based on reviewer feedback.
- Iteration logic confusion in test orchestrator with sequential directory numbering.
- Test failures by accepting both `query:text` and `--query text` as equivalent.
- Skill loading in headless test mode to ensure proper skill availability.
- Test scope ambiguity in scenarios and expectations.

## [1.1.0] - 2025-11-15

### Changed

- **BREAKING: Test infrastructure redesigned** - Replaced 3-tier agent hierarchy (167 context loads) with Python orchestrator (80 context loads), reducing test time from 60s+ to ~6s per test.
- testing-gh-skills skill documentation updated to reflect Python orchestrator approach.
- testing-gh-skills marked as SLASH COMMAND ONLY to prevent accidental expensive test runs.
- Enhanced using-gh-cli-search skill with mandatory directive style to prevent agents from bypassing skill system.

### Added

- Python test orchestrator (testing/scripts/run-all-tests.py) that parses scenarios, executes 80 tests with clean isolation, and generates 3-level reports.
- Test-reviewer agent for post-test analysis with root cause identification and prioritized recommendations.
- Execution timing metrics to all test suite reports (start time, end time, duration, average per test).
- Root .gitignore for Python, IDE, and OS files.
- Test reports .gitignore to exclude generated reports from git.

### Fixed

- Critical permission mode bug in run-single-test.sh (changed acceptAll to bypassPermissions), resolving 100% test failure rate.
- Test timeout issues by disabling episodic memory searches, increasing timeout to 120s, and adding concise output mode.
- Command extraction failures with enhanced regex patterns and support for setup/diagnostic commands.
- Test prompts improved for clarity with more explicit command requests.

### Improved

- Test pass rate from 70% to 73.8% (59/80 tests passing).
- Test execution speed from 60s+ timeouts to ~6s per test.
- Timeout rate from 30% to 0%.
- Skill tool invocation explicitly added to test runner to ensure skills are loaded during tests.

### Removed

- Five unused slash commands (/gh-search-code, /gh-search-commits, /gh-search-issues, /gh-search-prs, /gh-search-repos).
- Redundant .gitignore in testing/reports/ (moved to root).
- Old 3-tier agent hierarchy (test-orchestrator, test-group-leader, test-validator).

## [1.0.0] - 2025-11-15

### Added

- Initial public release of GitHub CLI Search plugin for Claude Code.
- Nine comprehensive skills: gh-search-code, gh-search-commits, gh-search-issues, gh-search-prs, gh-search-repos, gh-cli-setup, gh-search, testing-gh-skills, and using-gh-cli-search.
- Six slash commands for quick skill invocation: /gh-search-code, /gh-search-commits, /gh-search-issues, /gh-search-prs, /gh-search-repos, and /test-gh-skills.
- Three-tier hierarchical testing agent architecture (test-orchestrator, test-group-leader, test-validator).
- Session-start hook system with automatic using-gh-cli-search skill loading.
- Complete plugin structure following Claude Code specification with plugin manifest and marketplace catalog.
- Comprehensive test infrastructure with 80 test scenarios across 6 files validating syntax, quoting, exclusions, and platform requirements.
- Platform-specific handling for Unix/Linux/Mac and PowerShell environments.
- Critical syntax guidance for exclusion flags (-- for Unix, --% for PowerShell), quoting rules, @me special value, and ISO8601 date formats.
- Installation support for multiple methods (marketplace, direct clone, manual, team configuration).
- Documentation with examples, common mistakes reference, and best practices.
