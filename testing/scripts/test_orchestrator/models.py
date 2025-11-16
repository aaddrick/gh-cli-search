"""Data models for test orchestration"""

from datetime import datetime
from typing import Optional, List


class TestResult:
    """Test execution result with metadata"""

    def __init__(self, group: str, test_num: int, test_name: str, user_request: str):
        self.group = group
        self.test_num = test_num
        self.test_name = test_name
        self.user_request = user_request
        self.command_generated = ""
        self.status = "PENDING"
        self.failure_reason = ""
        self.output = ""
        self.criteria: List[str] = []
        self.platform = "All"
        self.duration_seconds = 0.0
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
