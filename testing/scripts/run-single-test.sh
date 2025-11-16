#!/bin/bash
# Run a single test using Claude Code headless mode
# This script provides a CLEAN test - only the user request, no hints
# Usage: ./run-single-test.sh <user-request>

set -e

USER_REQUEST="${1}"

if [ -z "$USER_REQUEST" ]; then
    echo "Usage: $0 <user-request>"
    echo "Example: $0 \"Find my open issues that are NOT labeled as bug\""
    exit 1
fi

# Execute Claude with ONLY the user request
# No test criteria, no hints - authentic skill application test
# Minimal tools to prevent slowdowns and hanging
# Read: Required for loading skills
# Skill: Required for using gh-cli-search skills
# bypassPermissions: Prevents interactive prompts
# NO episodic memory: Add explicit instruction to skip it
claude -p "CRITICAL INSTRUCTIONS:
1. Identify which gh-cli-search skill is needed: gh-search-code, gh-search-issues, gh-search-prs, gh-search-repos, gh-search-commits, or gh-cli-setup
2. Use the Skill tool to load that skill
3. Follow the skill's documentation to generate the correct command
4. Do not search episodic memory

USER REQUEST: ${USER_REQUEST}

Provide ONLY the gh command in a code block. No explanations." \
--output-format text \
--allowedTools "Read,Skill" \
--permission-mode bypassPermissions
