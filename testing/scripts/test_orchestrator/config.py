"""Configuration constants and paths for test orchestrator"""

from pathlib import Path
from threading import Lock

# Paths
REPO_ROOT = Path("/home/aaddrick/source/gh-cli-search")
SCENARIOS_DIR = REPO_ROOT / "testing" / "scenarios"
REPORTS_BASE = REPO_ROOT / "testing" / "reports"
RUN_TEST_SCRIPT = REPO_ROOT / "testing" / "scripts" / "run-single-test.sh"
TEST_REVIEWER_AGENT = REPO_ROOT / "agents" / "test-reviewer.md"
PRODUCT_MANAGER_AGENT = REPO_ROOT / "agents" / "product-manager.md"
DEVELOPER_AGENT = REPO_ROOT / "agents" / "developer.md"

# Thread-safe printing
print_lock = Lock()

# Maximum test iterations to prevent infinite loops
MAX_TEST_ITERATIONS = 5
