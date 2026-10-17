"""Interview set 4. Each problem is a working solution. Analyze the code exactly as written.
Fill in each answer block, then ask the tutor to grade. Assume CPython. SPACE means auxiliary
space (exclude the input; include recursion stack; count the output only if the problem says so).
"""
import heapq
from collections import defaultdict
from functools import lru_cache


# ═══ IV-16 ═══════════════════════════════════════════
# n = len(s), k = number of distinct characters in s
def iv16(s):
    """Problem: Given a string s, return the length of the longest substring without
    repeating characters.
    LeetCode: https://leetcode.com/problems/longest-substring-without-repeating-characters/
    """
    best = 0
    left = 0
    for right in range(len(s)):
        while s[right] in s[left:right]:
            left += 1
        best = max(best, right - left + 1)
    return best

# TIME:
# SPACE:
# WHY:
# SURE:


# ═══ IV-17 ═══════════════════════════════════════════
# m = len(grid) (rows), n = len(grid[0]) (columns)
def iv17(grid):
    """Problem: A warehouse robot starts at the top-left cell and must reach the bottom-right
    cell, moving only right or down. '#' cells are blocked, '.' cells are open. Return the
    number of distinct routes modulo 1_000_000_007.
    """
    m, n = len(grid), len(grid[0])
    MOD = 1_000_000_007

    @lru_cache(maxsize=None)
    def ways(r, c):
        if r >= m or c >= n or grid[r][c] == '#':
            return 0
        if r == m - 1 and c == n - 1:
            return 1
        return (ways(r + 1, c) + ways(r, c + 1)) % MOD

    return ways(0, 0)

# TIME:
# SPACE:
# WHY:
# SURE:


# ═══ IV-18 ═══════════════════════════════════════════
# V = len(services), E = len(deps)
def iv18(services, deps):
    """Problem: Deploy order for microservices. deps is a list of pairs (a, b) meaning a must
    be deployed before b. Return a valid deploy order containing every service, or None if
    the dependencies contain a cycle.
    """
    indeg = {s: 0 for s in services}
    graph = {s: [] for s in services}
    for a, b in deps:
        graph[a].append(b)
        indeg[b] += 1
    ready = [s for s in services if indeg[s] == 0]
    order = []
    while ready:
        s = ready.pop(0)
        order.append(s)
        for t in graph[s]:
            indeg[t] -= 1
            if indeg[t] == 0:
                ready.append(t)
    return order if len(order) == len(services) else None

# TIME:
# SPACE:
# WHY:
# SURE:


# ═══ IV-19 ═══════════════════════════════════════════
# n = number of pairs
def iv19(n):
    """Problem: Given n pairs of parentheses, return all combinations of well-formed
    parentheses.
    LeetCode: https://leetcode.com/problems/generate-parentheses/
    """
    result = []

    def build(cur, opened, closed):
        if len(cur) == 2 * n:
            result.append(cur)
            return
        if opened < n:
            build(cur + "(", opened + 1, closed)
        if closed < opened:
            build(cur + ")", opened, closed + 1)

    build("", 0, 0)
    return result

# TIME:
# SPACE:
# WHY:
# SURE:


# ═══ IV-20 ═══════════════════════════════════════════
# V = n (number of nodes), E = len(times)
def iv20(times, n, k):
    """Problem: A network has n nodes labeled 1..n. times[i] = (u, v, w) is a directed edge
    from u to v taking w >= 0 time. A signal is sent from node k. Return the time for all
    nodes to receive it, or -1 if some node never does.
    LeetCode: https://leetcode.com/problems/network-delay-time/
    """
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))
    dist = {}
    heap = [(0, k)]
    while heap:
        d, u = heapq.heappop(heap)
        if u in dist:
            continue
        dist[u] = d
        for v, w in graph[u]:
            if v not in dist:
                heapq.heappush(heap, (d + w, v))
    return max(dist.values()) if len(dist) == n else -1

# TIME:
# SPACE:
# WHY:
# SURE:
