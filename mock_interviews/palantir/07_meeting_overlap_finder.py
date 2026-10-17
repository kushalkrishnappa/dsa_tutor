"""
Questions:
- if there are no meetings I will return empty []. Is that okay?
- will there be repeatition of the meetings with same start and end time for same user?
- Are the meetings sorted by start time or end time or name?
- Can I assume the user will always be lowercase english letters?
- Do I have to clearn the values of trailing whitespaces or can I assume it is clean?

Approach:
- line sweep algorithm
"""

import heapq
from datetime import datetime

def str_to_utc(date_time: str) -> str:
    """Format datetime from string to UTC."""
    return datetime.fromisoformat(date_time)

def to_events(meetings: dict) -> list[tuple]:
    """Parse meetings to events of type [start, end, user].
    Time: O(NlogN)
    Space: O(N)
    """
    events = []
    for meet in meetings:
        start, end = str_to_utc(meet["start"]), str_to_utc(meet["end"])
        if start < end:
            events.append((start, end, meet["user"]))
    events.sort()
    return events

def find_overlapping_pairs(meetings: list[dict]) -> list[tuple[str, str]]:
    """
    Finds all user pairs with at least one pair of overlapping meetings.

    Args:
        meetings: list of meeting dicts with 'user', 'start', 'end' (ISO 8601 with offset).

    Returns:
        Sorted list of (user_a, user_b) tuples where user_a < user_b.

    Time: O(NlogN + P), N = size of meerings
    Space: O(N + sort)
    """
    if not meetings:
        return []

    overlaps = set()
    events = to_events(meetings=meetings)
    active = []

    for start, end, user in events:
        while active and active[0][0] <= start:
            heapq.heappop(active)
        for _, other_user in active:
            if other_user != user:
                overlaps.add((min(user, other_user), max(user, other_user)))
        heapq.heappush(active, (end, user))
    return sorted(overlaps)

meetings = [
    {"user": "alice", "start": "2024-03-15T09:00:00+00:00", "end": "2024-03-15T10:00:00+00:00"},
    {"user": "bob",   "start": "2024-03-15T09:30:00+00:00", "end": "2024-03-15T11:00:00+00:00"},
    {"user": "carol", "start": "2024-03-15T10:00:00+00:00", "end": "2024-03-15T11:00:00+00:00"},
    {"user": "alice", "start": "2024-03-15T14:00:00+00:00", "end": "2024-03-15T15:00:00+00:00"},
    {"user": "carol", "start": "2024-03-15T14:30:00+00:00", "end": "2024-03-15T15:30:00+00:00"},
]

print(find_overlapping_pairs(meetings=meetings))
