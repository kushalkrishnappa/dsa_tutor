"""Fill in each answer block, then ask the tutor to grade. Placeholder helpers like
do_constant_work() are O(1) unless a comment states otherwise. SPACE means auxiliary space
(exclude the input) unless the problem says otherwise.
"""
from itertools import combinations


# ─── DL-01 ───────────────────────────────────────────
# n = len(nums)
def dl01(nums, target):
    hits = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                hits += 1
                break
    return hits

# ALSO: give best-case time too
# TIME:
# SPACE:
# BEST:
# WHY:
# SURE:


# ─── DL-02 ───────────────────────────────────────────
# n = number of nodes in a heap-indexed tree (root = 1, parent of v = v // 2)
def dl02(n):
    total_depth = 0
    for node in range(1, n + 1):
        cur = node
        while cur > 1:
            cur //= 2
            total_depth += 1
    return total_depth

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── DL-03 ───────────────────────────────────────────
# n = len(points), m = len(centers)
# dist(p, q) is O(1)
def dl03(points, centers):
    assignment = [0] * len(points)
    for _ in range(10):
        for i, p in enumerate(points):
            best = 0
            for c in range(1, len(centers)):
                if dist(p, centers[c]) < dist(p, centers[best]):
                    best = c
            assignment[i] = best
    return assignment

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── DL-04 ───────────────────────────────────────────
# n = len(readings)
def dl04(readings):
    n = len(readings)
    peaks = []
    stride = 1
    while stride < n:
        best = readings[0]
        for i in range(0, n, stride):
            best = max(best, readings[i])
        peaks.append(best)
        stride *= 2
    return peaks

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── DL-05 ───────────────────────────────────────────
# n = len(tasks)
def dl05(tasks):
    pending = list(tasks)
    rounds = 0
    while pending:
        for t in pending:
            do_constant_work(t)
        pending.pop()
        rounds += 1
    return rounds

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── DL-06 ───────────────────────────────────────────
# n = len(s), k = max number of distinct characters allowed (k >= 1)
def dl06(s, k):
    counts = {}
    left = best = 0
    for right, ch in enumerate(s):
        counts[ch] = counts.get(ch, 0) + 1
        while len(counts) > k:
            counts[s[left]] -= 1
            if counts[s[left]] == 0:
                del counts[s[left]]
            left += 1
        best = max(best, right - left + 1)
    return best

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── DL-07 ───────────────────────────────────────────
# n is a positive int; treat integer arithmetic and shifts as O(1)
def dl07(n):
    width = 1
    while (1 << width) < n:
        width *= 2
    return width

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── DL-08 ───────────────────────────────────────────
# n is a positive int
def dl08(n):
    divisor_count = [0] * (n + 1)
    for d in range(1, n + 1):
        for multiple in range(d, n + 1, d):
            divisor_count[multiple] += 1
    return max(divisor_count)

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── DL-09 ───────────────────────────────────────────
# n = len(nums)
def dl09(nums):
    zero_triples = 0
    for a, b, c in combinations(nums, 3):
        if a + b + c == 0:
            zero_triples += 1
    return zero_triples

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── DL-10 ───────────────────────────────────────────
# n is a positive int
def dl10(n):
    most = 0
    for x in range(1, n + 1):
        count = 0
        d = 1
        while d * d <= x:
            if x % d == 0:
                count += 1 if d * d == x else 2
            d += 1
        most = max(most, count)
    return most

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── DL-11 ───────────────────────────────────────────
# n = len(s)
def dl11(s):
    longest = 0
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        longest = max(longest, j - i)
        i = j
    return longest

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── DL-12 ───────────────────────────────────────────
# n = len(values)
def dl12(values):
    if not values:
        return 0
    level = list(values)
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level), 2):
            right = level[i + 1] if i + 1 < len(level) else 0
            nxt.append(level[i] + right)
        level = nxt
    return level[0]

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── DL-13 ───────────────────────────────────────────
# n = len(prefix) - 1   (prefix[i] = sum of the first i values)
def dl13(prefix):
    n = len(prefix) - 1
    best = 0
    for size in range(1, n + 1):
        for start in range(0, n - size + 1, size):
            best = max(best, prefix[start + size] - prefix[start])
    return best

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── DL-14 ───────────────────────────────────────────
# n = number of coins
def dl14(n):
    rows = 0
    used = 0
    while used + (rows + 1) <= n:
        rows += 1
        used += rows
    return rows

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── DL-15 ───────────────────────────────────────────
# n = len(nums); nums is sorted ascending
def dl15(nums):
    n = len(nums)
    total = 0
    for x in nums:
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] < 2 * x:
                lo = mid + 1
            else:
                hi = mid
        total += lo
    return total

# TIME:
# SPACE:
# WHY:
# SURE:
