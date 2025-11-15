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
claude -p "IMPORTANT: Be concise. Do not search episodic memory. Do not explain - just provide the command.

USER REQUEST: ${USER_REQUEST}

Provide ONLY the gh command in a code block. No explanations." \
--output-format text \
--allowedTools "Read,Skill" \
--permission-mode bypassPermissions
