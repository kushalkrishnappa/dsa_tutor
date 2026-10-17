# Keys — interview_set_3.py (tutor only — learner does not open)

Conventions for this file: dict/set/deque operations are expected O(1) **plus the cost of hashing
the key** (O(len) for a fresh str/tuple; single characters and short names are O(1)). SPACE is
auxiliary: the input is excluded, and the returned value is excluded unless the problem statement
says it counts. A learner who separately and correctly states the output size gets credit for that
too.

## IV-11
- **Trick:** monotonic-stack
- **Secondary tricks:** two-pointer-nested-while
- **Source:** LeetCode sliding-window-maximum
- **Hidden inefficiency:** none
- **Difficulty:** 2/3
- **Time:** Θ(n), independent of k
- **Space:** Θ(k) auxiliary (the deque never holds more than k indices; `out` is the output,
  n−k+1 values)
- **ONE STEP:** Θ(k) worst case for a single iteration. The `while` can pop every index in the
  deque, up to k of them, e.g. after a strictly decreasing run when a new maximum arrives.
- **Why:** Every index is appended once and removed at most once, by either `pop` or `popleft`.
  So the total number of `while` iterations over the whole run is ≤ n, even though one iteration
  can pay Θ(k): aggregate Θ(n), amortized Θ(1) per step. The `popleft` check keeps only indices
  > i−k, so the deque size is ≤ k.
- **Common wrong answers:** Θ(n·k) (sees a `while` inside a `for` and multiplies by the deque's
  maximum size). Θ(n log k) (recalls the heap solution). Space Θ(n) — Partial (valid, but the
  window bound k is what the code guarantees). ONE STEP Θ(1) (confuses amortized with worst-case
  single-step cost).
- **Probe questions:** "Give an input where a single step pops k−1 or more indices." → e.g. k, k−1,
  …, 1 followed by a huge value. "Why can the total pops not exceed n?" → each index is pushed exactly
  once, and you can't pop what wasn't pushed (aggregate/accounting argument).
- **Variant seeds:** daily-temperatures (next greater element, monotonic stack, Θ(n)); shortest
  subarray with sum ≥ K using a monotonic deque of prefix sums.
- **Verified:** derivation ×2 + empirical op-count (vary n → n; vary k with n fixed → constant total;
  max pops in one step vs k → k; deque peak vs k → k)
- **Retired:** —

## IV-12
- **Trick:** path-copy-recursion
- **Secondary tricks:** stack-depth-vs-total-calls, multi-variable-bound
- **Source:** original
- **Hidden inefficiency:** `chain + [r]` builds a brand-new list at every call. Mutating one shared
  list (append before the call, pop after, copy once when found) gives Θ(N) time and Θ(h) space.
- **Difficulty:** 3/3
- **Time:** Θ(N·h) worst case (target absent, or found last)
- **Space:** Θ(h²) (h active frames; the frame at depth d holds its own chain of length d+1, so
  1 + 2 + … + h)
- **Why:** The DFS visits each employee at most once, and reaching a node at depth d first copies a
  chain of length d (`chain + [r]` is O(d)). So the time is Σ over visited nodes of depth ≤ N·h. A
  "broom" (a manager chain of length h with the remaining N−h employees all reporting to the last
  manager) makes ≈ (N−h)·h of that copying unavoidable. Space: the copies along the current
  root-to-node path are all alive at once, Σ_{d≤h} d = Θ(h²). Siblings' chains are freed when their
  call returns. In a balanced org h = Θ(log N), so this is Θ(N log N) / Θ(log² N). For a single
  chain (h = N) it's Θ(N²) / Θ(N²).
- **Common wrong answers:** Θ(N) time (standard DFS answer — ignores the per-call list copy).
  Θ(h) space (counts frames, not the chain each frame owns). Θ(N²) time — Partial (valid upper bound
  since h ≤ N, but drops the variable that matters). Θ(N·h) space (thinks every chain ever built is
  kept alive).
- **Probe questions:** "In a balanced org of a million people, does this matter?" → h ≈ 20, so the
  overhead is only a factor of ~20. It hurts on deep, chain-like orgs. "Which line would you change
  to get Θ(N) time and Θ(h) space?" → append r to one shared list before recursing, pop after, and
  return `list(chain)` once on success.
- **Variant seeds:** all root-to-leaf paths with a given sum (output-sensitive, copying only at
  leaves vs at every call); maze path recovery passing `path + [(r, c)]` on a grid.
- **Verified:** derivation ×2 + empirical op-count (broom tree: vary N with h fixed → N; vary h with
  N fixed → h; peak elements held by live chains vs h → h²)
- **Retired:** —

## IV-13
- **Trick:** trie-total-chars
- **Secondary tricks:** —
- **Source:** LeetCode implement-trie-prefix-tree
- **Hidden inefficiency:** none
- **Difficulty:** 1/3
- **Time:** Θ(q·L) worst case. More precisely Θ(T) where T = total characters across all ops,
  and T ≤ q·L. Both forms Pass.
- **Space:** Θ(q·L) worst case: one dict node per character of every inserted word when no
  prefixes are shared. More precisely, the number of distinct prefixes inserted.
- **Why:** Each op walks its word one character at a time, and each step is an O(1) dict
  get/insert keyed by a single character. Search/startsWith may stop early, but the worst case
  walks the whole word. Space: `setdefault` creates a node only for a new (prefix, char) step, so
  at most one node per inserted character.
- **Common wrong answers:** Θ(q) ("dict ops are O(1)" — forgets the per-character walk). Θ(q·L·26)
  — Pass on time (constant factor), but a Miss if the learner insists the 26 is a growing variable.
  Space Θ(26^L) (confuses the possible trie size with the actual one). Space Θ(q) (one node per
  word instead of per character).
- **Probe questions:** "If all q words were the same, what's the space?" → Θ(L), a single path.
  "Why doesn't each node cost 26 slots here?" → nodes are dicts holding only the children that
  exist. An array-of-26 implementation would make the space Θ(26·q·L) = still Θ(q·L), with a larger
  constant.
- **Variant seeds:** longest common prefix via a trie (Θ(total chars)); replace-words with a trie
  vs. checking every prefix slice against a set (Θ(L²) per word).
- **Verified:** derivation ×2 + empirical op-count (vary q → q; vary L → L; trie nodes created vs
  total inserted chars → linear)
- **Retired:** —

## IV-14
- **Trick:** builtin-in-loop
- **Secondary tricks:** multi-variable-bound
- **Source:** original
- **Hidden inefficiency:** a full `sorted()` of every player after every event just to read the top
  entry. A max-heap of (−score, name, version) with lazy deletion of stale entries (or a sorted
  container) gives Θ(q log q).
- **Difficulty:** 3/3
- **Time:** Θ(q·u·log u) (Θ(q² log q) when every event is a new player)
- **Space:** Θ(u) (`scores`, plus the `ranking` list and its u key tuples during each sort; `leaders`
  is output)
- **Why:** After event i the dict holds u_i ≤ u players, and `sorted` over them is Θ(u_i log u_i).
  The dict is in insertion order, not score order, so Timsort gets no free sorted runs in general.
  Once all u players have appeared, every remaining event pays Θ(u log u), and the first u events
  cost only Σ i log i ≤ u² log u ≤ q·u log u. So the total is Θ(q·u log u). The key lambda builds u
  tuples per sort, Θ(u), which is dominated.
- **Common wrong answers:** Θ(q log q) (thinks it's "one sort", or counts only the dict update).
  Θ(q·u) (forgets the log of the sort). Θ(q² log q) — Partial (valid since u ≤ q, but loses u). Θ(q)
  (reads `ranking[0]` as an O(1) max).
- **Probe questions:** "Would `max(scores.items(), key=…)` instead of `sorted(...)[0]` change the
  bound?" → yes, Θ(q·u): a linear scan per event instead of a sort. "If points were always
  positive, how cheap could it be?" → only the updated player can overtake, so compare against the
  current leader: Θ(q).
- **Variant seeds:** median of a stream by re-sorting after every insert (Θ(q² log q) vs two-heap
  Θ(q log q)); "top 3 products after each sale" with `sorted(...)[:3]` in the loop (vs a k-heap).
- **Verified:** derivation ×2 + empirical op-count (comparison-counting key wrapper; vary q with u
  fixed → q; vary u with q fixed → u log u)
- **Retired:** —

## IV-15
- **Trick:** geometric-inner-loop
- **Secondary tricks:** slice-copy, multi-variable-bound
- **Source:** original
- **Hidden inefficiency:** none
- **Difficulty:** 2/3
- **Time:** Θ(n), independent of C
- **Space:** Θ(min(n, C)) (the largest slice/payload: ≤ 2C, since a size above C fails and is
  halved, and ≤ n)
- **Why:** Slicing and joining a batch both cost O(len(batch)). While size ≤ C, the sizes double
  (1, 2, 4, …), so the ramp costs a geometric sum. After that the pattern repeats: success at s (≤ C,
  advancing s records), double to 2s, fail, halve back to s. Each record advanced therefore pays its
  own copy plus at most a share of a failed batch twice as large: ≤ ~3n copying in total. The number
  of attempts is Θ(log min(n, C) + n/C), each O(1) plus its slice.
- **Common wrong answers:** Θ(log n) (counts doubling steps and ignores the slice/join work).
  Θ(n log n) (log n rounds × "a slice of n"). Θ(n·C) or Θ(n²) (thinks failures make it re-send
  everything). Space Θ(1) (forgets the slice copies) or Θ(n) — Partial (true when C ≥ n, but the
  cap bounds every batch).
- **Probe questions:** "How many send attempts are made for n = 10⁶, C = 1000?" → ≈ 10 ramp attempts,
  then about 2 attempts per 512 records advanced (s = 512 is the largest power of two ≤ 1000): ≈ 2·10⁶/512
  ≈ 4,000. "What if a rejection reset the size to 1 instead of halving?" → each cycle re-ramps
  1, 2, …, s: still Θ(n) copying (the ramp is geometric), but Θ((n/C)·log C) attempts.
- **Variant seeds:** dynamic-array resize simulation with copy-on-grow (amortized Θ(1) append);
  exponential search (gallop 1, 2, 4… then binary search) on a sorted list, using slices vs indices.
- **Verified:** derivation ×2 + empirical op-count (vary n → n; vary C with n fixed → constant;
  largest slice vs C → C; largest slice vs n with huge C → n)
- **Retired:** —
