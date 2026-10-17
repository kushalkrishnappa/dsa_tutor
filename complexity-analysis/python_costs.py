"""Fill in each answer block, then ask the tutor to grade. Assume CPython. Placeholder helpers
like do_constant_work() are O(1) unless a comment states otherwise. SPACE means auxiliary space
(exclude the input) unless the problem says otherwise.
"""
import copy
import heapq
from collections import Counter


# ─── PY-01 ───────────────────────────────────────────
# n = len(s), k = window length (1 <= k <= n)
def py01(s, k):
    seen = set()
    repeated = set()
    for i in range(len(s) - k + 1):
        chunk = s[i:i + k]
        if chunk in seen:
            repeated.add(chunk)
        seen.add(chunk)
    return len(repeated)

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── PY-02 ───────────────────────────────────────────
# n = len(nums)
def py02(nums):
    order = sorted(nums)
    ranks = []
    for x in nums:
        ranks.append(order.index(x) + 1)
    return ranks

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── PY-03 ───────────────────────────────────────────
# n = number of nodes in the binary tree (nodes have .val, .left, .right)
def py03(root):
    def dfs(node, path):
        if node is None:
            return 0
        path = path + [node.val]
        if node.left is None and node.right is None:
            return 1 if path == path[::-1] else 0
        return dfs(node.left, path) + dfs(node.right, path)

    return dfs(root, [])

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── PY-04 ───────────────────────────────────────────
# n = len(s)
def py04(s):
    cleaned = ""
    for ch in s:
        if ch.isalnum():
            cleaned += ch.lower()
    return cleaned == cleaned[::-1]

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── PY-05 ───────────────────────────────────────────
# n = len(nums), k = how many distinct values to collect (1 <= k <= n)
def py05(nums, k):
    first = {}
    for i, x in enumerate(nums):
        if len(first) == k:
            break
        if x not in first.keys():
            first[x] = i
    return list(first.keys())

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── PY-06 ───────────────────────────────────────────
# n = len(nums)
def py06(nums):
    total = 0
    rest = nums
    while rest:
        total += rest[0]
        rest = rest[1:]
    return total

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── PY-07 ───────────────────────────────────────────
# n = len(stream)
def py07(stream):
    seen = []
    medians = []
    for x in stream:
        seen.append(x)
        ordered = sorted(seen)
        medians.append(ordered[len(ordered) // 2])
    return medians

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── PY-08 ───────────────────────────────────────────
# V = number of nodes, E = number of edges; graph maps each node to a list of neighbors
def py08(graph, start):
    dist = {start: 0}
    queue = [start]
    while queue:
        u = queue.pop(0)
        for v in graph[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                queue.append(v)
    return dist

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── PY-09 ───────────────────────────────────────────
# n = len(nums), k = how many of the largest values to return (1 <= k <= n)
def py09(nums, k):
    heap = [-x for x in nums]
    heapq.heapify(heap)
    top = []
    for _ in range(k):
        top.append(-heapq.heappop(heap))
    return top

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── PY-10 ───────────────────────────────────────────
# n = len(nums)
def py10(nums):
    unique = []
    for x in nums:
        if x not in unique:
            unique.append(x)
    return unique

# ALSO: give best-case time too
# TIME:
# SPACE:
# BEST:
# WHY:
# SURE:


# ─── PY-11 ───────────────────────────────────────────
# board is r x c, m = len(moves); count the returned list in SPACE
def py11(board, moves):
    history = []
    for i, j in moves:
        board[i][j] = 1
        history.append(copy.deepcopy(board))
    return history

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── PY-12 ───────────────────────────────────────────
# n = len(s)
def py12(s):
    if len(s) <= 1:
        return True
    if s[0] != s[-1]:
        return False
    return py12(s[1:-1])

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── PY-13 ───────────────────────────────────────────
# n = len(nums)
def py13(nums):
    count = 0
    for x in nums:
        if x == max(nums):
            count += 1
    return count

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── PY-14 ───────────────────────────────────────────
# n = len(s), k = len(p)  (1 <= k <= n)
def py14(s, p):
    need = Counter(p)
    matches = 0
    for i in range(len(s) - len(p) + 1):
        if Counter(s[i:i + len(p)]) == need:
            matches += 1
    return matches

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── PY-15 ───────────────────────────────────────────
# n = len(nums), nums is non-empty
def py15(nums):
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best

# TIME:
# SPACE:
# WHY:
# SURE:
