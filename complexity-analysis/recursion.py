"""Fill in each answer block, then ask the tutor to grade. Placeholder helpers like
do_constant_work() are O(1) unless a comment states otherwise. SPACE means auxiliary space
(exclude the input) unless the problem says otherwise; the recursion stack counts.
"""
import math


# ─── RR-01 ───────────────────────────────────────────
# n = len(players); stronger(a, b) is O(1)
def rr01(players):
    if len(players) == 1:
        return players[0]
    next_round = []
    for i in range(0, len(players) - 1, 2):
        next_round.append(stronger(players[i], players[i + 1]))
    if len(players) % 2 == 1:
        next_round.append(players[-1])          # odd one out gets a bye
    return rr01(next_round)

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── RR-02 ───────────────────────────────────────────
# n = number of nodes in the singly linked list starting at head
def rr02(head):
    def walk(node, running_total):
        if node is None:
            return running_total
        return walk(node.next, running_total + node.val)
    return walk(head, 0)

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── RR-03 ───────────────────────────────────────────
# n = len(tracks); adjust(tracks, i) is O(1)
def rr03(tracks):
    def rebalance(lo, hi):                      # works on positions lo .. hi-1
        if hi - lo < 3:
            return
        for i in range(lo, hi):
            adjust(tracks, i)
        cut = lo + (hi - lo) // 3
        rebalance(lo, cut)
        rebalance(cut, hi)
    rebalance(0, len(tracks))

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── RR-04 ───────────────────────────────────────────
# n = len(features); score(chosen) is O(len(chosen))
def rr04(features):
    best = [float("-inf")]
    chosen = []

    def explore(i):
        if i == len(features):
            best[0] = max(best[0], score(chosen))
            return
        chosen.append(features[i])
        explore(i + 1)
        chosen.pop()
        explore(i + 1)

    explore(0)
    return best[0]

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── RR-05 ───────────────────────────────────────────
# n = number of stairs; step_cost(i) is O(1)
_rr05_memo = {}                                 # module-level; empty before the first call

def rr05(n):
    if n <= 1:
        return 0
    if n in _rr05_memo:
        return _rr05_memo[n]
    best = min(rr05(n - 1) + step_cost(n - 1),
               rr05(n - 2) + step_cost(n - 2))
    _rr05_memo[n] = best
    return best

# ALSO: give the time of an immediate second call rr05(n) with the same n
# TIME:
# SPACE:
# SECOND CALL:
# WHY:
# SURE:


# ─── RR-06 ───────────────────────────────────────────
# n = len(points); compare(p, q) is O(1)
def rr06(points):
    def sweep(lo, hi):                          # works on positions lo .. hi-1
        size = hi - lo
        if size < 4:
            return
        for i in range(lo, hi):
            for j in range(i + 1, hi):
                compare(points[i], points[j])
        half, quarter = size // 2, size // 4
        sweep(lo, lo + half)
        sweep(lo + quarter, lo + quarter + half)
        sweep(hi - half, hi)
    sweep(0, len(points))

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── RR-07 ───────────────────────────────────────────
# n = length of the access code (an int); counts n-bit codes with no two adjacent 1s
def rr07(n):
    def count(remaining, last_was_one):
        if remaining == 0:
            return 1
        total = count(remaining - 1, False)     # place a 0
        if not last_was_one:
            total += count(remaining - 1, True)  # place a 1
        return total
    return count(n, False)

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── RR-08 ───────────────────────────────────────────
# u = universe size (an int, not a list); math.isqrt is O(1) here
def rr08(u):
    if u <= 2:
        return 0
    cluster_size = math.isqrt(u)
    write_level_header(cluster_size)
    return 1 + rr08(cluster_size)

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── RR-09 ───────────────────────────────────────────
# n = len(queue)
def rr09(queue):
    def settle(k):                              # moves the largest of the first k to index k-1
        if k <= 1:
            return
        top = 0
        for i in range(1, k):
            if queue[i] > queue[top]:
                top = i
        queue[top], queue[k - 1] = queue[k - 1], queue[top]
        settle(k - 1)
    settle(len(queue))

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── RR-10 ───────────────────────────────────────────
# n = len(guests); snapshot(lst) returns a copy of lst in O(len(lst))
# SPACE for this problem: include the returned list
def rr10(guests):
    seatings = []

    def arrange(k):
        if k == len(guests):
            seatings.append(snapshot(guests))
            return
        for i in range(k, len(guests)):
            guests[k], guests[i] = guests[i], guests[k]
            arrange(k + 1)
            guests[k], guests[i] = guests[i], guests[k]

    arrange(0)
    return seatings

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── RR-11 ───────────────────────────────────────────
# n = len(nums); partition(nums, lo, hi) costs O(hi - lo + 1) and returns the pivot's
# final index p, where lo <= p <= hi -- you do not control where p lands
def rr11(nums):
    def sort(lo, hi):
        while lo < hi:
            p = partition(nums, lo, hi)
            if p - lo < hi - p:
                sort(lo, p - 1)
                lo = p + 1
            else:
                sort(p + 1, hi)
                hi = p - 1
    sort(0, len(nums) - 1)

# ALSO: give best-case time too
# TIME:
# SPACE:
# BEST:
# WHY:
# SURE:


# ─── RR-12 ───────────────────────────────────────────
# n = len(heights)
def rr12(heights):
    def tallest(lo, hi):                        # inclusive range lo .. hi
        if lo == hi:
            return heights[lo]
        mid = (lo + hi) // 2
        return max(tallest(lo, mid), tallest(mid + 1, hi))
    return tallest(0, len(heights) - 1)

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── RR-13 ───────────────────────────────────────────
# n = len(jobs); there are always exactly 3 servers
def rr13(jobs):
    loads = [0, 0, 0]
    best = [float("inf")]

    def assign(i):
        if i == len(jobs):
            best[0] = min(best[0], max(loads))
            return
        for s in range(3):
            loads[s] += jobs[i]
            assign(i + 1)
            loads[s] -= jobs[i]

    assign(0)
    return best[0]

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── RR-14 ───────────────────────────────────────────
# n = len(nums), k = number of pieces, 2 <= k <= n // 2; nums are non-negative
def rr14(nums, k):
    n = len(nums)
    suffix = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix[i] = suffix[i + 1] + nums[i]
    memo = {}

    def best(i, pieces):                        # smallest possible largest-piece sum from i on
        if pieces == 1:
            return suffix[i]
        if (i, pieces) in memo:
            return memo[(i, pieces)]
        answer, running = float("inf"), 0
        for j in range(i, n - pieces + 1):
            running += nums[j]
            answer = min(answer, max(running, best(j + 1, pieces - 1)))
        memo[(i, pieces)] = answer
        return answer

    return best(0, k)

# TIME:
# SPACE:
# WHY:
# SURE:


# ─── RR-15 ───────────────────────────────────────────
# n = len(scores)
def rr15(scores):
    flips = 0

    def sort(lo, hi):                           # sorts positions lo .. hi-1 in place
        nonlocal flips
        if hi - lo < 2:
            return
        mid = (lo + hi) // 2
        sort(lo, mid)
        sort(mid, hi)
        merged, i, j = [], lo, mid
        while i < mid or j < hi:
            if j == hi or (i < mid and scores[i] <= scores[j]):
                merged.append(scores[i]); i += 1
            else:
                flips += mid - i
                merged.append(scores[j]); j += 1
        for t in range(len(merged)):
            scores[lo + t] = merged[t]

    sort(0, len(scores))
    return flips

# TIME:
# SPACE:
# WHY:
# SURE:
