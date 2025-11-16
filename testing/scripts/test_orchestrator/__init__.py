"""Test orchestrator package for gh-cli-search test suite execution"""

from .orchestration import main
from .models import TestResult

__all__ = ['main', 'TestResult']
