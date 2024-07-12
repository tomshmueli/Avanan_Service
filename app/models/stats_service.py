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

        # Custom binary search logic to only consider the first element (timestamp)
        # by that we assure that the search is done only on the timestamps
        # Binary search saves us iterating over the whole list of timestamps
        low, high = 0, len(stats_time)
        while low < high:
            mid = (low + high) // 2
            if stats_time[mid][0] > end:
                high = mid
            else:
                low = mid + 1

        end_index = low

        if end_index == 0:
            return {keyword: 0 for keyword in KEYWORDS}

        return stats_time[end_index - 1][1]
