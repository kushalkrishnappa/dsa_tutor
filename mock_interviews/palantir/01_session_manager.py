import heapq
import random

class SessionManager:
    """
    - Will I get the set of servers initially as a param to the SessionManager class?
    - Can you provide me an overview of what these interfaces should do and who uses it?
    - What do you want me to do if the initial requests are less than len(servers)? 
    How do you want me to allocate in this case? Does servers get priority?
    - What will be the maximum number of sessions that should be handled?
    """

    def __init__(self, servers: list[str]):
        self.servers = servers
        self.priority = []
        self._sessions = {}
        self._build_priority()

    def _build_priority(self):
        """
        Time: O(N)
        Space: O(N)
        """
        for server in self.servers:
            heapq.heappush(self.priority, (0, server))

    def _get_priority(self) -> tuple[int, str]:
        """
        Time: O(logN)    
        Space: O(1) auxilarry
        """
        session_count, server = None, None
        if self.priority:
            session_count, server = heapq.heappop(self.priority)
        return (session_count, server)

    def _set_priority(self, sessions_count: int, server: str) -> None:
        """
        Time: O(logN)    
        Space: O(1) auxilarry
        """
        heapq.heappush(self.priority, (sessions_count, server))

    def start_session(self, session_id: str) -> None:
        """
        Time: O(logn)
        Space: O(1)
        """
        if not self.servers:
            return
        if session_id in self._sessions:
            return
        sessions_count, server = self._get_priority()
        self._sessions[session_id] = server
        self._set_priority(sessions_count + 1, server)

    def get_allocation(self) -> dict[str, set[str]]:
        """
        Time: O(N)
        Space: O(1) auxilary space
        """
        allocations = {server: set() for server in self.servers}
        for session_id, server in self._sessions.items():
            allocations[server].add(session_id)
        return allocations

class DynamicSessionManager:
    """
    Follow-ups 1, 2, 4.

    Lazy deletion: the heap may hold stale (key, server) entries. An entry is
    live only if the server is still active and the key matches its current
    load. Every load change pushes a fresh entry; stale ones are skipped when
    they surface at the root. No rebuild on add/remove/end.

    No migration: after end_session / add_server the gap can exceed 1 for a
    while; every new session goes to the least-loaded server, closing it.
    """

    def __init__(self, servers: list[str]):
        self.count = {server: 0 for server in servers}  # active servers only
        self.alloc = {server: set() for server in servers}
        self.owner = {}  # session_id -> server, O(1) lookup on end_session
        self.heap = [self._entry(server) for server in servers]
        heapq.heapify(self.heap)

    def _key(self, server: str):
        return self.count[server]

    def _entry(self, server: str) -> tuple:
        return (self._key(server), server)

    def _is_live(self, entry: tuple) -> bool:
        _, server = entry
        return server in self.count and entry == self._entry(server)

    def _push(self, server: str) -> None:
        """
        Time: O(logH), H = heap size (amortized O(logN) with compaction)
        """
        heapq.heappush(self.heap, self._entry(server))
        if len(self.heap) > 2 * len(self.count) + 16:  # mostly stale -> compact
            self.heap = [self._entry(s) for s in self.count]
            heapq.heapify(self.heap)

    def _least_loaded(self) -> str | None:
        while self.heap and not self._is_live(self.heap[0]):
            heapq.heappop(self.heap)
        return self.heap[0][1] if self.heap else None

    def start_session(self, session_id: str) -> None:
        """
        Time: O(logN) amortized
        """
        if session_id in self.owner:
            return
        server = self._least_loaded()
        if server is None:
            return
        self.alloc[server].add(session_id)
        self.owner[session_id] = server
        self.count[server] += 1
        self._push(server)  # old entry is now stale

    def end_session(self, session_id: str) -> None:
        """
        Follow-up 2: O(1) find via owner, then push the decremented count.
        The id can be started again afterwards.
        Time: O(logN) amortized
        """
        server = self.owner.pop(session_id, None)
        if server is None:
            return
        self.alloc[server].remove(session_id)
        self.count[server] -= 1
        self._push(server)

    def add_server(self, server: str) -> None:
        """
        Follow-up 1: new server starts at 0, so it is the root for a while.
        Time: O(logN)
        """
        if server in self.count:
            return
        self.count[server] = 0
        self.alloc[server] = set()
        self._push(server)

    def remove_server(self, server: str) -> None:
        """
        Follow-up 1: mark inactive (its heap entries go stale), then re-place
        its sessions on the least-loaded servers.
        Time: O(S logN), S = sessions on the removed server
        """
        if server not in self.count:
            return
        del self.count[server]
        orphans = self.alloc.pop(server)
        for session_id in orphans:
            del self.owner[session_id]
        for session_id in orphans:
            self.start_session(session_id)

    def get_allocation(self) -> dict[str, set[str]]:
        """
        Follow-up 4: deep copy, so callers can mutate the result freely.
        Tradeoff: O(N + T) time and memory per call, T = total sessions.
        MappingProxyType alone is not enough: it guards the outer dict, but
        the inner sets would still be ours, and a live view changes under the reader.
        """
        return {server: set(sessions) for server, sessions in self.alloc.items()}


class WeightedSessionManager(DynamicSessionManager):
    """
    Follow-up 3: balance load proportional to capacity.
    Only the heap key changes: count / capacity, tie broken by server_id.
    """

    def __init__(self, capacities: dict[str, int]):
        self.capacity = dict(capacities)
        super().__init__(list(capacities))

    def _key(self, server: str) -> float:
        return self.count[server] / self.capacity[server]

    def add_server(self, server: str, capacity: int = 1) -> None:
        if server in self.count:
            return
        self.capacity[server] = capacity
        super().add_server(server)


class RoundRobinSessionManager:
    """
    Follow-up 5: small, fixed server set -> O(1) per start_session.
    Cycling s1, s2, s3, s1, ... keeps counts within 1 of each other.
    Breaks once sessions end or servers change: a freed slot isn't refilled first.
    """

    def __init__(self, servers: list[str]):
        self.servers = sorted(servers)
        self.next = 0
        self.alloc = {server: set() for server in self.servers}
        self.seen = set()

    def start_session(self, session_id: str) -> None:
        """
        Time: O(1)
        """
        if not self.servers or session_id in self.seen:
            return
        self.seen.add(session_id)
        self.alloc[self.servers[self.next]].add(session_id)
        self.next = (self.next + 1) % len(self.servers)

    def get_allocation(self) -> dict[str, set[str]]:
        return {server: set(sessions) for server, sessions in self.alloc.items()}


def counts(alloc: dict[str, set[str]]) -> dict[str, int]:
    return {server: len(sessions) for server, sessions in alloc.items()}


if __name__ == "__main__":
    # Base question
    sm = SessionManager(["s1", "s2", "s3"])
    for sid in ["a", "a", "b", "c", "d", "e", "f"]:
        sm.start_session(sid)
    alloc = sm.get_allocation()
    assert sorted(len(v) for v in alloc.values()) == [2, 2, 2]
    assert set().union(*alloc.values()) == {"a", "b", "c", "d", "e", "f"}

    # Follow-up 1: add/remove servers at runtime
    dm = DynamicSessionManager(["s1", "s2"])
    for sid in "abcd":
        dm.start_session(sid)
    dm.add_server("s3")
    dm.start_session("e")
    dm.start_session("f")
    assert counts(dm.get_allocation()) == {"s1": 2, "s2": 2, "s3": 2}
    dm.remove_server("s1")
    alloc = dm.get_allocation()
    assert counts(alloc) == {"s2": 3, "s3": 3}
    assert set().union(*alloc.values()) == set("abcdef")
    dm.start_session("g")  # stale s1 entries are skipped
    assert "s1" not in dm.get_allocation()

    # Follow-up 2: end_session
    dm = DynamicSessionManager(["s1", "s2", "s3"])
    for sid in "abcdef":
        dm.start_session(sid)
    freed = dm.owner["a"]
    dm.end_session("a")
    dm.end_session("zzz")  # unknown id -> no-op
    dm.start_session("g")
    assert dm.owner["g"] == freed  # freed server is least loaded
    dm.start_session("a")  # ended ids can be reused
    assert "a" in dm.owner

    # Follow-up 3: weighted by capacity
    wm = WeightedSessionManager({"big": 2, "small": 1})
    for i in range(30):
        wm.start_session(str(i))
    assert counts(wm.get_allocation()) == {"big": 20, "small": 10}

    # Follow-up 4: caller mutations don't leak in
    alloc = dm.get_allocation()
    alloc["s1"].add("hacked")
    alloc["s9"] = set()
    assert "hacked" not in dm.alloc["s1"] and "s9" not in dm.alloc

    # Follow-up 5: round robin
    rr = RoundRobinSessionManager(["s3", "s1", "s2"])
    for sid in ["a", "a", "b", "c", "d", "e", "f", "g"]:
        rr.start_session(sid)
    assert counts(rr.get_allocation()) == {"s1": 3, "s2": 2, "s3": 2}

    # Random ops: every new session lands on a least-loaded server
    rng = random.Random(0)
    dm = DynamicSessionManager(["s0", "s1", "s2"])
    next_server = 3
    for _ in range(5000):
        op = rng.random()
        if op < 0.5:
            sid = str(rng.randrange(200))
            before = dict(dm.count)
            dm.start_session(sid)
            if before and sid in dm.owner and dm.count != before:
                assert before[dm.owner[sid]] == min(before.values())
        elif op < 0.85:
            dm.end_session(str(rng.randrange(200)))
        elif op < 0.93:
            dm.add_server(f"s{next_server}")
            next_server += 1
        elif dm.count:
            dm.remove_server(rng.choice(sorted(dm.count)))
        assert counts(dm.alloc) == dm.count
        assert {sid for s in dm.alloc.values() for sid in s} == set(dm.owner)
        assert len(dm.heap) <= 2 * len(dm.count) + 17

    print("all tests passed")
