"""Fill in each answer block, then ask the tutor to grade. Placeholder helpers like
do_constant_work() are O(1) unless a comment states otherwise. SPACE means auxiliary space
(exclude the input) unless the problem says otherwise.
"""
import heapq
from collections import deque


# ─── AM-01 ───────────────────────────────────────────
# n = len(commands); each command is ("job", x) or ("print",)
def am01(commands):
    incoming, outgoing = [], []
    printed = []
    for cmd in commands:
        if cmd[0] == "job":
            incoming.append(cmd[1])
        else:
            if not outgoing:
                while incoming:
                    outgoing.append(incoming.pop())
            if outgoing:
                printed.append(outgoing.pop())
    return printed

# ALSO: worst-case cost of handling one single "print" command
# TIME:
# SPACE:
# SINGLE-OP:
# WHY:
# SURE:


# ─── AM-02 ───────────────────────────────────────────
# m = number of rows, n = number of columns, L = len(word)
def am02(board, word):
    m, n = len(board), len(board[0])

    def walk(r, c, i):
        if i == len(word):
            return True
        if not (0 <= r < m and 0 <= c < n) or board[r][c] != word[i]:
            return False
        saved, board[r][c] = board[r][c], "#"
        found = (walk(r + 1, c, i + 1) or walk(r - 1, c, i + 1) or
                 walk(r, c + 1, i + 1) or walk(r, c - 1, i + 1))
        board[r][c] = saved
        return found

    return any(walk(r, c, 0) for r in range(m) for c in range(n))

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── AM-03 ───────────────────────────────────────────
# n = len(words), S = total number of characters across all words
def am03(words):
    root = {}
    distinct_prefixes = 0
    for w in words:
        node = root
        for ch in w:
            if ch not in node:
                node[ch] = {}
                distinct_prefixes += 1
            node = node[ch]
    return distinct_prefixes

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── AM-04 ───────────────────────────────────────────
# n = number of servers (labelled 0..n-1), m = len(cables)
def am04(n, cables):
    parent = list(range(n))
    rank = [0] * n

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    clusters = n
    for a, b in cables:
        ra, rb = find(a), find(b)
        if ra != rb:
            if rank[ra] < rank[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            if rank[ra] == rank[rb]:
                rank[ra] += 1
            clusters -= 1
    return clusters

# ALSO: worst-case cost of one single find() call
# TIME:
# SPACE:
# SINGLE-OP:
# WHY:
# SURE:


# ─── AM-05 ───────────────────────────────────────────
# V = number of build steps (0..V-1), E = len(must_precede)
def am05(V, must_precede):
    unlocks = [[] for _ in range(V)]
    waiting_on = [0] * V
    for before, after in must_precede:
        unlocks[before].append(after)
        waiting_on[after] += 1
    ready = deque(s for s in range(V) if waiting_on[s] == 0)
    order = []
    while ready:
        s = ready.popleft()
        order.append(s)
        for t in unlocks[s]:
            waiting_on[t] -= 1
            if waiting_on[t] == 0:
                ready.append(t)
    return order if len(order) == V else []

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── AM-06 ───────────────────────────────────────────
# n = len(rows), k = chunk (1 <= k <= n)
class Ledger:
    def __init__(self, chunk):
        self.chunk = chunk
        self.cap = 0
        self.size = 0
        self.block = []

    def add(self, row):
        if self.size == self.cap:
            self.cap += self.chunk
            bigger = [None] * self.cap
            for i in range(self.size):
                bigger[i] = self.block[i]
            self.block = bigger
        self.block[self.size] = row
        self.size += 1


def am06(rows, k):
    ledger = Ledger(k)
    for row in rows:
        ledger.add(row)
    return ledger

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── AM-07 ───────────────────────────────────────────
# n = len(scores), k = number of winners requested (1 <= k <= n)
def am07(scores, k):
    podium = []
    for s in scores:
        if len(podium) < k:
            heapq.heappush(podium, s)
        elif s > podium[0]:
            heapq.heapreplace(podium, s)
    return sorted(podium, reverse=True)

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── AM-08 ───────────────────────────────────────────
# V = number of junctions, E = number of one-way roads; roads[u] = list of (v, minutes), minutes >= 0
def am08(roads, home):
    best = {home: 0}
    frontier = [(0, home)]
    settled = set()
    while frontier:
        t, u = heapq.heappop(frontier)
        if u in settled:
            continue
        settled.add(u)
        for v, minutes in roads[u]:
            arrive = t + minutes
            if arrive < best.get(v, float("inf")):
                best[v] = arrive
                heapq.heappush(frontier, (arrive, v))
    return best

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── AM-09 ───────────────────────────────────────────
# n = len(heights)
def am09(heights):
    bars = heights + [0]
    stack = []                      # (start_index, height)
    biggest = 0
    for i, h in enumerate(bars):
        start = i
        while stack and stack[-1][1] >= h:
            start, tall = stack.pop()
            biggest = max(biggest, tall * (i - start))
        stack.append((start, h))
    return biggest

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── AM-10 ───────────────────────────────────────────
# m = number of rows, n = number of columns
def am10(grid):
    m, n = len(grid), len(grid[0])
    seen = set()
    islands = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] == "#" and (r, c) not in seen:
                islands += 1
                seen.add((r, c))
                q = deque([(r, c)])
                while q:
                    cr, cc = q.popleft()
                    for nr, nc in ((cr + 1, cc), (cr - 1, cc), (cr, cc + 1), (cr, cc - 1)):
                        if (0 <= nr < m and 0 <= nc < n and grid[nr][nc] == "#"
                                and (nr, nc) not in seen):
                            seen.add((nr, nc))
                            q.append((nr, nc))
    return islands

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── AM-11 ───────────────────────────────────────────
# n = number of people (labelled 0..n-1), m = len(reports_to_pairs), m >= n
def am11(n, reports_to_pairs):
    boss = list(range(n))

    def top(x):
        while boss[x] != x:
            x = boss[x]
        return x

    for a, b in reports_to_pairs:
        ta, tb = top(a), top(b)
        if ta != tb:
            boss[ta] = tb
    return len({top(p) for p in range(n)})

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── AM-12 ───────────────────────────────────────────
# n = len(stream)
class Buf:
    def __init__(self):
        self.cap = 1
        self.size = 0
        self.slots = [None]

    def push(self, x):
        if self.size == self.cap:
            self.cap = self.cap + self.cap // 2 + 1
            fresh = [None] * self.cap
            for i in range(self.size):
                fresh[i] = self.slots[i]
            self.slots = fresh
        self.slots[self.size] = x
        self.size += 1


def am12(stream):
    buf = Buf()
    for x in stream:
        buf.push(x)
    return buf

# ALSO: worst-case cost of a single push()
# TIME:
# SPACE:
# SINGLE-OP:
# WHY:
# SURE:


# ─── AM-13 ───────────────────────────────────────────
# V = len(matrix) (matrix is V x V of 0/1), E = number of 1-entries; the network is sparse (E is about V)
def am13(matrix, start):
    V = len(matrix)
    nbrs = [[j for j in range(V) if matrix[i][j]] for i in range(V)]
    seen = [False] * V
    seen[start] = True
    stack = [start]
    reached = 0
    while stack:
        u = stack.pop()
        reached += 1
        for v in nbrs[u]:
            if not seen[v]:
                seen[v] = True
                stack.append(v)
    return reached

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── AM-14 ───────────────────────────────────────────
# n = len(plates), k = length of the longest plate string
def am14(plates):
    groups = {}
    for p in plates:
        signature = "".join(sorted(p))
        groups.setdefault(signature, []).append(p)
    return [g for g in groups.values() if len(g) > 1]

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── AM-15 ───────────────────────────────────────────
# n = len(weights), W = max(weights)
def am15(weights, days):
    def fits(cap):
        trucks, load = 1, 0
        for w in weights:
            if load + w > cap:
                trucks += 1
                load = 0
            load += w
        return trucks <= days

    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        if fits(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo

# TIME:
# SPACE:
# WHY:
# SURE:
