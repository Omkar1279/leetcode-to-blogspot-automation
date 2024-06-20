from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class LeetCodeSubmission:
    title: str
    url: str
    submission_date: datetime
    status: str
    tags: List[str] = None  # Assuming tags can be extracted
