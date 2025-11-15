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
claude -p "${USER_REQUEST}" \
--output-format text \
--allowedTools "Read" \
--permission-mode acceptAll
