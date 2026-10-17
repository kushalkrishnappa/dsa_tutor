# Keys — interview_set_2.py (tutor only — learner does not open)

Conventions for this file: dict/set operations are expected O(1) **plus the cost of hashing the
key** (O(len) for a fresh str/tuple). Arithmetic on numbers ≤ max(piles) is O(1). SPACE is
auxiliary: the input is excluded, and the returned value is excluded unless the problem statement
says it counts (IV-06 says it does).

## IV-06
- **Trick:** grid-bfs
- **Secondary tricks:** multi-variable-bound
- **Source:** original
- **Hidden inefficiency:** none
- **Difficulty:** 2/3
- **Time:** Θ(m·n), independent of s
- **Space:** Θ(m·n) (the `dist` grid, which the statement counts, plus a queue that can hold up to
  m·n cells, e.g. when every cell is a station)
- **Why:** The initial scan is Θ(m·n). After that it's a single multi-source BFS: a cell is enqueued
  only when its `dist` goes from −1 to a value, which happens at most once per cell. So there are
  ≤ m·n pops, each checking 4 neighbors. Putting all s stations in the queue at the start means
  each cell is reached once from its nearest station, not once per station.
- **Common wrong answers:** Θ(s·m·n) (pictures one BFS per station). Θ((m·n)²) (thinks each cell
  runs its own search for the nearest station). Θ(m + n) space for the queue (true of the frontier
  of a one-source BFS on an open grid, but not in the worst case here, and `dist` counts anyway).
- **Probe questions:** "What would the code look like if it really were Θ(s·m·n)?" → loop over the
  stations, run a fresh BFS from each, and take the min per cell. "Why does seeding the queue with
  every station give correct nearest distances?" → BFS pops cells in nondecreasing distance from the
  *set* of sources, so it acts like one virtual source connected to all stations.
- **Variant seeds:** rotting oranges (minutes until all rot, multi-source); walls-and-gates; 0/1 BFS
  on a grid where some moves cost 0 (deque appendleft).
- **Verified:** derivation ×2 + empirical op-count (vary m·n → linear; vary s on a fixed grid →
  constant; queue peak with all stations → m·n)
- **Retired:** —

## IV-07
- **Trick:** slice-recursion
- **Secondary tricks:** geometric-inner-loop, stack-depth-vs-total-calls
- **Source:** original
- **Hidden inefficiency:** each call copies half of its list (`arr[mid + 1:]` / `arr[:mid]`).
  Passing `lo`/`hi` indices into the original list would give Θ(log n) time and Θ(1) space
  iteratively (Θ(log n) stack if recursive).
- **Difficulty:** 3/3
- **Time:** Θ(n)
- **Space:** Θ(n): the slices still referenced by active frames add up to n/2 + n/4 + … < n.
  There are Θ(log n) frames.
- **Why:** T(n) = T(n/2) + Θ(n), because the slice copies ≈ n/2 elements. The work per level halves:
  n/2 + n/4 + … = Θ(n), so the copying swamps the log n comparisons. Each frame keeps its own
  `arr` alive until the recursion returns (it's a return-call, but CPython has no tail-call
  elimination), so the live slices also sum to Θ(n). This holds in every case. Even when the
  answer is found quickly, the first call already copies n/2.
- **Common wrong answers:** Θ(log n) time (recognizes binary search, ignores the slices).
  Θ(n log n) (log n levels × "n for the slice" — forgets that the slices halve). Space Θ(log n)
  (counts only stack frames, not the slice each frame holds). Space Θ(1) (thinks the
  return-call is tail-call optimized).
- **Probe questions:** "Rewrite the recurrence and solve it." → T(n) = T(n/2) + cn ⇒ cn(1 + ½ + ¼ +
  …) ≤ 2cn. "If it kept the slices but also did a linear `sum(arr)` sanity check in every call?"
  → still T(n/2) + Θ(n) = Θ(n). A full scan per level only gives n log n when both halves recurse.
- **Variant seeds:** recursive "is sorted" check `ok(a) = a[0] <= a[1] and ok(a[1:])` (Θ(n²) time,
  Θ(n²) space); quickselect that slices the chosen side (average Θ(n) still, but now Θ(n) space).
- **Verified:** derivation ×2 + empirical op-count (copied elements fit n; peak elements held by
  live slices fit n)
- **Retired:** —

## IV-08
- **Trick:** binary-search-on-answer
- **Secondary tricks:** multi-variable-bound
- **Source:** LeetCode koko-eating-bananas
- **Hidden inefficiency:** none
- **Difficulty:** 1/3
- **Time:** Θ(n·log M)
- **Space:** Θ(1)
- **Why:** The search is over speeds 1..M, not over the array, so it runs ≈ log₂ M iterations.
  Each iteration recomputes the hours with a full Θ(n) pass. `max(piles)` adds one more Θ(n).
  h affects only which half is kept, never how many iterations run.
- **Common wrong answers:** Θ(n log n) (assumes the binary search is over indices of `piles`).
  Θ(n·M) (pictures trying every speed). Θ(log M) (forgets the inner pass). Θ(n log h) (thinks the
  search is over hours).
- **Probe questions:** "Piles go up to 10⁹ and n up to 10⁴. Roughly how many operations?" →
  ≈ 30 × 10⁴ = 3×10⁵. "What property of `hours(speed)` makes binary search valid?" → it's
  monotonically non-increasing in the speed, so the feasible speeds form a suffix [k*, M].
- **Variant seeds:** capacity to ship packages within D days (lo = max(w), hi = sum(w): n log(sum));
  split array largest sum; minimize max distance to gas station (real-valued search, iterations
  set by precision).
- **Verified:** derivation ×2 + empirical op-count (vary n → linear; vary log₂ M → linear in log M)
- **Retired:** —

## IV-09
- **Trick:** union-find
- **Secondary tricks:** —
- **Source:** LeetCode redundant-connection
- **Hidden inefficiency:** `find` has neither path compression nor union by rank/size, so trees can
  degrade into chains. With both, the time is Θ(n·α(n)) (effectively linear); with either one alone
  it's O(n log n).
- **Difficulty:** 2/3
- **Time:** Θ(n²) worst case
- **Space:** Θ(n) (the `parent` array)
- **Why:** Each `find` walks parent pointers to the root, which is O(n) hops at most, and there are
  2n finds, so O(n²). The bound is reached by edges (1,2), (1,3), …, (1,n), then (2,3).
  `parent[find(1)] = find(v)` hangs the old root under v each time, so node 1 sits at the bottom of a
  chain that grows by one per edge, and the i-th edge's `find(1)` takes ≈ i hops. That totals ≈ n²/2.
- **Common wrong answers:** Θ(n·α(n)) or "Θ(n), union-find is basically O(1)" (quotes the textbook
  union-find bound without checking that this `find` does no compression and that unions ignore
  rank). Θ(n log n) (would be right with union by rank alone — not what's written).
- **Probe questions:** "Add `parent[x] = find(parent[x])`-style compression only. New worst case?"
  → O(n log n) total (amortized O(log n) per op). With union by rank as well → Θ(n·α(n)). "Does the
  input order matter for this code?" → yes; e.g. edges (i, i+1) in order make every find O(1).
- **Variant seeds:** count connected components (number-of-provinces) with the same naive find; Kruskal
  MST with naive union-find (sorting E log E would no longer be the bottleneck).
- **Verified:** derivation ×2 + empirical op-count on the chain-building edge order (fits n²)
- **Retired:** —

## IV-10
- **Trick:** hash-key-cost
- **Secondary tricks:** —
- **Source:** original
- **Hidden inefficiency:** none
- **Difficulty:** 1/3
- **Time:** Θ(n·k)
- **Space:** Θ(n·k) (up to n distinct k-tuples kept in `seen`; `dups` is output)
- **Why:** For each row, `tuple(row)` copies k references in Θ(k). The `in` and `add` calls each
  hash the tuple, and CPython does not cache tuple hashes, so that's Θ(k) per call. A hash hit also
  runs an element-by-element equality check, Θ(k). So each row costs Θ(k). When every row is
  distinct, `seen` stores n tuples of k slots each.
- **Common wrong answers:** Θ(n) time ("set lookups are O(1)" — true per lookup only when the key
  has constant size). Θ(n) space (counts set entries, not the k items inside each). Θ(n²·k)
  (thinks `in seen` compares against every stored row).
- **Probe questions:** "Why does the code need `tuple(row)` at all?" → lists are mutable and
  unhashable. "If each cell were a string of up to c characters, what changes?" → hashing a tuple
  hashes each element, which costs O(c) for a fresh string → Θ(n·k·c) (strings cache their hash
  after the first time, so strings shared between rows would be cheaper).
- **Variant seeds:** count distinct islands by storing a tuple of each island's normalized cell
  offsets (Θ(m·n) total); detect repeated board states in a game simulation keyed by
  `tuple(map(tuple, board))`.
- **Verified:** derivation ×2 + empirical timing of the real function (vary k with n fixed → k; vary n
  with k fixed → n)
- **Retired:** —
