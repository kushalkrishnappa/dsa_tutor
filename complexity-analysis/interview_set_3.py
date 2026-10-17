"""Interview set 3. Each problem is a working solution. Analyze the code exactly as written.
Fill in each answer block, then ask the tutor to grade. Assume CPython. SPACE means auxiliary
space (exclude the input; include recursion stack; count the output only if the problem says so).
"""
from collections import deque


# ═══ IV-11 ═══════════════════════════════════════════
# n = len(nums), k = window size (1 <= k <= n)
def iv11(nums, k):
    """Problem: Given an array nums and a window of size k sliding from left to right one
    position at a time, return the maximum of each window.
    LeetCode: https://leetcode.com/problems/sliding-window-maximum/
    """
    dq = deque()                  # indices; their values are decreasing front to back
    out = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:        # front index has left the window
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out

# ALSO: worst-case cost of ONE iteration of the for loop (not averaged)
# TIME:
# SPACE:
# ONE STEP:
# WHY:
# SURE:


# ═══ IV-12 ═══════════════════════════════════════════
# N = number of employees, h = height of the org tree (longest manager chain)
def iv12(reports, ceo, target):
    """Problem: reports maps each employee to the list of their direct reports (employees with
    no reports may be missing from the dict). Return the chain of command from the CEO down
    to target as a list of names, or None if target is not in the org.
    """
    def dfs(person, chain):
        if person == target:
            return chain
        for r in reports.get(person, []):
            found = dfs(r, chain + [r])
            if found:
                return found
        return None

    return dfs(ceo, [ceo])

# TIME:
# SPACE:
# WHY:
# SURE:


# ═══ IV-13 ═══════════════════════════════════════════
# q = len(ops), L = length of the longest word in ops
def iv13(ops):
    """Problem: Implement a trie supporting insert(word), search(word) -> bool (exact word
    was inserted) and startsWith(prefix) -> bool. Here ops is a list such as
    [("insert", "apple"), ("search", "app"), ("startsWith", "app")]; return the list of
    results (None for inserts). Words are lowercase letters.
    LeetCode: https://leetcode.com/problems/implement-trie-prefix-tree/
    """
    END = "$"
    root = {}
    out = []
    for op, word in ops:
        node = root
        if op == "insert":
            for ch in word:
                node = node.setdefault(ch, {})
            node[END] = True
            out.append(None)
            continue
        for ch in word:
            if ch not in node:
                node = None
                break
            node = node[ch]
        if node is None:
            out.append(False)
        elif op == "search":
            out.append(END in node)
        else:
            out.append(True)
    return out

# TIME:
# SPACE:
# WHY:
# SURE:


# ═══ IV-14 ═══════════════════════════════════════════
# q = len(updates), u = number of distinct players
def iv14(updates):
    """Problem: Live game leaderboard. updates is a list of (player, points) events in time
    order; each adds points (possibly negative, for penalties) to that player's score, and
    new players start at 0. After every event, record the current leader: highest score,
    ties broken by name. Return the list of leaders.
    """
    scores = {}
    leaders = []
    for player, pts in updates:
        scores[player] = scores.get(player, 0) + pts
        ranking = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
        leaders.append(ranking[0][0])
    return leaders

# TIME:
# SPACE:
# WHY:
# SURE:


# ═══ IV-15 ═══════════════════════════════════════════
# n = len(records), C = cap (largest batch the server accepts, C >= 1)
def iv15(records, cap):
    """Problem: Upload a list of short string records with "slow start" batching. The server
    rejects any batch larger than cap records, but the client does not know cap. Start with
    a batch size of 1; after an accepted batch, double the size; after a rejected batch,
    halve the size (minimum 1) and retry from the same position. Return the number of send
    attempts and the total characters transmitted (rejected batches included).
    """
    def send(batch):                     # stand-in for the network call
        payload = ",".join(batch)        # serialize: O(len(batch))
        return len(batch) <= cap, len(payload)

    i, size, attempts, chars_sent = 0, 1, 0, 0
    while i < len(records):
        batch = records[i:i + size]
        ok, sent = send(batch)
        attempts += 1
        chars_sent += sent
        if ok:
            i += len(batch)
            size *= 2
        else:
            size = max(1, size // 2)
    return attempts, chars_sent

# TIME:
# SPACE:
# WHY:
# SURE:
