import time
from typing import Dict, List, Tuple
import bisect
from app.models.event_service import EventService
from app.models.event import KEYWORDS


class StatsService:
    def __init__(self, event_service: EventService):
        self.event_service = event_service

    def get_stats(self, start: int = None, end: int = None) -> Dict[str, int]:
        if start is None and end is None:
            raise ValueError("No interval provided")

        current_time = int(time.time() - self.event_service.start_time)
        if start is None:  # interval = [0, end]
            start = 0
        if end is None:  # interval = [0, current_time - start]
            end = current_time - start
            start = 0

        if start >= end:
            raise ValueError("Invalid interval: start time must be before end time.")

        stats_time = self.event_service.get_stats_time()
        end_index = bisect.bisect_right(stats_time, (end, {}))

        return stats_time[end_index - 1][1]
