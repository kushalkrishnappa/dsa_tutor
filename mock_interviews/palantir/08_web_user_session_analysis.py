"""


"""

import heapq

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Session:
    user_id: str
    name: str
    login_time: datetime
    logout_time: datetime

def format_duration(total_seconds: int) -> str:
    total_minutes = total_seconds // 60
    hours, minutes = total_minutes // 60, total_minutes % 60
    return f"{hours}h {minutes}m"

def top_users_by_time(sessions: list[Session], k: int = 3) -> list[tuple[str, str, str]]:
    """
    Returns up to k users as (user_id, name, formatted_duration),
    sorted by total time desc, then name asc, then user_id asc.
    e.g. [("u2", "Bob", "2h 15m"), ("u1", "Alice", "1h 30m")]
    """
    total_time = defaultdict(int)
    name = {}
    for session in sessions:
        login_time, logout_time = session.login_time, session.logout_time
        if not (login_time and logout_time and logout_time > login_time):
            continue
        total_time[session.user_id] += int((logout_time - login_time).total_seconds())
        name[session.user_id] = session.name

    top_k = heapq.nsmallest(k, total_time.items(), key=lambda item: (-item[1], name[item[0]], item[0]))

    return [(uid, name[uid], format_duration(total)) for uid, total in top_k]


from datetime import timedelta
T0 = datetime(2024, 5, 1, 9, 0)
def at(minutes: int) -> datetime:
    return T0 + timedelta(minutes=minutes)

sessions = [
    Session("u3", "Cara", at(0), at(20)),
    Session("u1", "Alice", at(100), at(145)),
    Session("u2", "Bob", at(0), at(120)),
    Session("u3", "Cara", at(200), at(220)),
    Session("u4", "Dan", at(0), at(10)),
    Session("u1", "Alice", at(0), at(30)),
    Session("u3", "Cara", at(300), at(320)),
]

print(top_users_by_time(sessions=sessions, k=3))