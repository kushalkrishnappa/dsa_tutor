"""Interview set 1. Each problem is a working solution. Analyze the code exactly as written.
Fill in each answer block, then ask the tutor to grade. Assume CPython. SPACE means auxiliary
space (exclude the input; include recursion stack; count the output only if the problem says so).
"""
from collections import defaultdict


# ═══ IV-01 ═══════════════════════════════════════════
# n = len(s), m = len(word_dict), L = length of the longest word in word_dict
def iv01(s, word_dict):
    """Problem: Given a string s and a list of dictionary words, return True if s can be
    segmented into a sequence of one or more dictionary words (a word may be reused).
    LeetCode: https://leetcode.com/problems/word-break/
    """
    words = set(word_dict)
    longest = max(len(w) for w in word_dict)
    n = len(s)
    can = [False] * (n + 1)      # can[i]: s[:i] is segmentable
    can[0] = True
    for end in range(1, n + 1):
        for start in range(max(0, end - longest), end):
            if can[start] and s[start:end] in words:
                can[end] = True
                break
    return can[n]

# TIME:
# SPACE:
# WHY:
# SURE:


# ═══ IV-02 ═══════════════════════════════════════════
# n = horizon, m = len(intervals)
def iv02(intervals, horizon):
    """Problem: A monitoring system has m servers. Server i sends a heartbeat every
    intervals[i] seconds (at t = p, 2p, 3p, ... for p = intervals[i]). The intervals are
    distinct integers in 1..horizon. Over seconds 1..horizon, return the busiest second
    (most heartbeats, earliest on ties) and its heartbeat count.
    """
    hits = [0] * (horizon + 1)
    for p in intervals:
        for t in range(p, horizon + 1, p):
            hits[t] += 1
    busiest = 1
    for t in range(2, horizon + 1):
        if hits[t] > hits[busiest]:
            busiest = t
    return busiest, hits[busiest]

# TIME:
# SPACE:
# WHY:
# SURE:


# ═══ IV-03 ═══════════════════════════════════════════
# n = len(nums)
def iv03(nums):
    """Problem: Given an array nums of distinct integers, return all possible permutations,
    in any order.
    LeetCode: https://leetcode.com/problems/permutations/
    """
    result = []
    path = []

    def backtrack():
        if len(path) == len(nums):
            result.append(path[:])
            return
        for x in nums:
            if x in path:
                continue
            path.append(x)
            backtrack()
            path.pop()

    backtrack()
    return result

# TIME:
# SPACE:
# WHY:
# SURE:


# ═══ IV-04 ═══════════════════════════════════════════
# n = len(strs), k = length of the longest string
def iv04(strs):
    """Problem: Given an array of strings, group the anagrams together. Return the groups
    in any order.
    LeetCode: https://leetcode.com/problems/group-anagrams/
    """
    groups = defaultdict(list)
    for s in strs:
        key = "".join(sorted(s))
        groups[key].append(s)
    return list(groups.values())

# TIME:
# SPACE:
# WHY:
# SURE:


# ═══ IV-05 ═══════════════════════════════════════════
# n = len(digits)
def iv05(digits):
    """Problem: A finance export gives account balances as raw digit strings (no sign, no
    leading zeros). Format a balance with commas as thousands separators,
    e.g. "1234567" -> "1,234,567" and "999" -> "999".
    """
    out = ""
    count = 0
    for i in range(len(digits) - 1, -1, -1):
        if count == 3:
            out = "," + out
            count = 0
        out = digits[i] + out
        count += 1
    return out

# TIME:
# SPACE:
# WHY:
# SURE:
