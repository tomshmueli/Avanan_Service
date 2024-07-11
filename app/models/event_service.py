import re
from typing import Dict, List, Tuple
import time
from datetime import datetime, timezone
from app.models.event import KEYWORDS


class TimeService:
    @staticmethod
    def current_time() -> float:
        return datetime.now(timezone.utc).timestamp()


class EventService:
    def __init__(self):
        self.start_time = TimeService.current_time()
        self.keyword_counts = {keyword: 0 for keyword in KEYWORDS}
        self.stats_time: List[Tuple[int, Dict[str, int]]] = []
        print("EventService initialized. Data reset.")

    def process_event(self, sentence: str):
        """
        Process the event and store the keyword counts.
        Handle with corner cases such as: case-insensitive, whole word match, keyword substring inside another word.
        """
        elapsed_time = int(time.time() - self.start_time)
        for keyword in KEYWORDS:
            self.keyword_counts[keyword] += len(re.findall(rf'\b{keyword}\b', sentence.lower()))
        self.stats_time.append((elapsed_time, self.keyword_counts.copy()))
        print("Stored Events with Time:", self.stats_time)  # Temporary debug statement

    def get_keyword_counts(self) -> Dict[str, int]:
        return self.keyword_counts

    def get_stats_time(self) -> List[Tuple[int, Dict[str, int]]]:
        return self.stats_time
