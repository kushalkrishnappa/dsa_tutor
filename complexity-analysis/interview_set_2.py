"""Interview set 2. Each problem is a working solution. Analyze the code exactly as written.
Fill in each answer block, then ask the tutor to grade. Assume CPython. SPACE means auxiliary
space (exclude the input; include recursion stack; count the output only if the problem says so).
"""
from collections import deque


# ═══ IV-06 ═══════════════════════════════════════════
# m = len(grid) (rows), n = len(grid[0]) (columns), s = number of 'C' cells
def iv06(grid):
    """Problem: A warehouse floor is a grid of 'C' (charging station), '.' (open floor) and
    '#' (shelf). For every cell, compute the number of 4-directional steps to the nearest
    charging station without passing through shelves; use -1 for shelves and unreachable
    cells. Return the distance grid (the output counts toward space).
    """
    m, n = len(grid), len(grid[0])
    dist = [[-1] * n for _ in range(m)]
    queue = deque()
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 'C':
                dist[r][c] = 0
                queue.append((r, c))
    while queue:
        r, c = queue.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if (0 <= nr < m and 0 <= nc < n and grid[nr][nc] != '#'
                    and dist[nr][nc] == -1):
                dist[nr][nc] = dist[r][c] + 1
                queue.append((nr, nc))
    return dist

# TIME:
# SPACE:
# WHY:
# SURE:


# ═══ IV-07 ═══════════════════════════════════════════
# n = len(builds)
def iv07(builds):
    """Problem: CI history. builds is a list of booleans in chronological order: every build
    passes (True) up to some point and fails (False) from then on. Return the index of the
    first failing build, or len(builds) if none fail.
    """
    def first_fail(arr, offset):
        if not arr:
            return offset
        mid = len(arr) // 2
        if arr[mid]:                      # still passing: answer is to the right
            return first_fail(arr[mid + 1:], offset + mid + 1)
        return first_fail(arr[:mid], offset)

    return first_fail(builds, 0)

# TIME:
# SPACE:
# WHY:
# SURE:


# ═══ IV-08 ═══════════════════════════════════════════
# n = len(piles), M = max(piles), h = hours available (h >= n)
def iv08(piles, h):
    """Problem: Koko has n piles of bananas and h hours. Each hour she picks one pile and eats
    up to k bananas from it (if the pile has fewer, she eats them all and waits out the hour).
    Return the minimum integer speed k that lets her finish within h hours.
    LeetCode: https://leetcode.com/problems/koko-eating-bananas/
    """
    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        hours = 0
        for p in piles:
            hours += (p + mid - 1) // mid
        if hours <= h:
            hi = mid
        else:
            lo = mid + 1
    return lo

# TIME:
# SPACE:
# WHY:
# SURE:


# ═══ IV-09 ═══════════════════════════════════════════
# n = len(edges) (the graph has n nodes labeled 1..n)
def iv09(edges):
    """Problem: A tree with n nodes labeled 1..n had one extra edge added. Given the n edges,
    return an edge that can be removed so the remaining graph is a tree. If there are
    several answers, return the one that occurs last in the input.
    LeetCode: https://leetcode.com/problems/redundant-connection/
    """
    parent = list(range(len(edges) + 1))

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru == rv:
            return [u, v]
        parent[ru] = rv
    return []

# TIME:
# SPACE:
# WHY:
# SURE:


# ═══ IV-10 ═══════════════════════════════════════════
# n = len(rows), k = number of cells per row
def iv10(rows):
    """Problem: A spreadsheet export has n rows, each a list of k integer cells. Return the
    indices of rows that exactly duplicate some earlier row, in increasing order.
    """
    seen = set()
    dups = []
    for i, row in enumerate(rows):
        key = tuple(row)
        if key in seen:
            dups.append(i)
        else:
            seen.add(key)
    return dups

# TIME:
# SPACE:
# WHY:
# SURE:
