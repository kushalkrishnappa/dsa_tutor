# Keys — interview_set_4.py (tutor only — learner does not open)

Conventions for this file: dict/set operations are expected O(1) **plus the cost of hashing the
key** (small tuples and ints are O(1)). heapq push/pop on a heap of size s is O(log s). SPACE is
auxiliary: the input is excluded, and the returned value is excluded unless the problem statement
says it counts. A learner who separately and correctly states the output size gets credit for that
too.

## IV-16
- **Trick:** slice-copy
- **Secondary tricks:** sliding-window-amortized, multi-variable-bound
- **Source:** LeetCode longest-substring-without-repeating-characters
- **Hidden inefficiency:** `s[right] in s[left:right]` copies the window and scans it on every
  check. A dict of each character's last index (jump `left` directly) or a set of window characters
  gives the optimal Θ(n).
- **Difficulty:** 3/3
- **Time:** Θ(n·k)
- **Space:** Θ(k) (one window slice at a time, and the window has no repeats, so its length is ≤ k)
- **Why:** The `while` condition runs ≤ 2n times in total: each run either moves `left` forward (≤ n
  times overall, the usual sliding-window amortization) or ends the loop (once per `right`). Each run
  copies and scans `s[left:right]`, whose length is ≤ k because a window with no repeats can't be
  longer than the number of distinct characters. That gives O(n·k). The cyclic string "abc…(k
  letters)abc…" reaches it: the window stays at length ≈ k, so every step pays ≈ 2k.
- **Common wrong answers:** Θ(n) (quotes the known optimal sliding-window bound, applying the
  amortization to the loop count but ignoring the O(window) cost of each check). Θ(n²) — Partial
  (valid upper bound since k ≤ n, but misses the k that the variables line defines). Θ(n·k²)
  (multiplies the window slice by the number of `while` iterations per step without the amortized
  2n total). Space Θ(1) or Θ(n) — Θ(n) is Partial, Θ(1) is a Miss (forgets the slice copy).
- **Probe questions:** "For lowercase-only input, what does this become?" → k ≤ 26, so Θ(26n) = Θ(n) —
  the inefficiency is only asymptotic for large alphabets (e.g. arbitrary Unicode, or integer
  arrays). "Why is the number of `while` checks O(n) in total, not O(n·k)?" → `left` only moves
  forward and never passes `right`, so the true-branch runs ≤ n times overall.
- **Variant seeds:** the same window kept as a list with `while x in window: window.pop(0)` (two
  hidden costs, still Θ(n·k)); longest subarray with at most two distinct values using
  `len(set(arr[l:r+1]))` in the loop (Θ(n²) worst).
- **Verified:** derivation ×2 + empirical op-count (cyclic k-letter string: vary n → n; vary k with n
  fixed → k)
- **Retired:** —

## IV-17
- **Trick:** two-dimensional-memo
- **Secondary tricks:** stack-depth-vs-total-calls
- **Source:** original
- **Hidden inefficiency:** none
- **Difficulty:** 2/3
- **Time:** Θ(m·n)
- **Space:** Θ(m·n) (the cache holds one entry per reachable (r, c), plus the out-of-range border
  states; the recursion stack adds Θ(m + n), which is dominated)
- **Why:** There are (m+1)(n+1) possible (r, c) arguments. `lru_cache` computes each at most once,
  and each body makes 2 calls, so ≤ 2(m+1)(n+1) calls in total. Hashing an (int, int) key is
  O(1), and `% MOD` keeps every count below 2³⁰, so the arithmetic is O(1). Each call increases r + c by 1, so
  the deepest chain is m + n frames.
- **Common wrong answers:** Θ(2^(m+n)) (analyzes the recursion tree as if there were no cache).
  Θ(C(m+n, m)) (counts paths, which is what the uncached version would enumerate). Space Θ(m + n)
  (counts only the stack and forgets the cache).
- **Probe questions:** "What happens on a 600×600 open grid?" → RecursionError: the depth ≈ m + n =
  1200 exceeds CPython's default limit of 1000 (verified: 480×480 runs, 520×520 fails). A bottom-up
  table, or a single rolling row (Θ(n) space), avoids it. "Without the `% MOD`, what would the cost
  be?" → the counts grow to ~C(m+n, m), i.e. Θ(m+n)-bit integers. Additions then cost Θ(m+n) each,
  so the time becomes Θ(m·n·(m+n)).
- **Variant seeds:** minimum path sum with memo (same state space); count paths when the robot may
  also move diagonally (3 transitions, same Θ(m·n)).
- **Verified:** derivation ×2 + empirical op-count (distinct states computed: vary m·n → linear; vary
  m with n fixed → m; max depth vs side → linear) + real `lru_cache` version run at 400×400
- **Retired:** —

## IV-18
- **Trick:** pop-front
- **Secondary tricks:** multi-variable-bound
- **Source:** original
- **Hidden inefficiency:** `ready.pop(0)` shifts every remaining element, so it's O(len(ready)).
  With `collections.deque` and `popleft()`, Kahn's algorithm is the optimal Θ(V + E).
- **Difficulty:** 2/3
- **Time:** Θ(V² + E) worst case
- **Space:** Θ(V + E) (`graph` holds E edges, and `indeg`, `ready`, `order` hold O(V) each)
- **Why:** Building the graph is Θ(V + E). Kahn's loop pops each service once and relaxes each edge
  once, Θ(V + E) — except that each `pop(0)` costs the current length of `ready`. With no
  dependencies (E = 0), all V services start ready, so the pops cost (V−1) + (V−2) + … = Θ(V²).
  In general it's ≤ V pops of ≤ V each, plus E.
- **Common wrong answers:** Θ(V + E) (quotes the textbook topological-sort bound, treating `pop(0)`
  as O(1)). Θ(V·E) (thinks each pop rescans all edges). Θ(E²) / Θ(V³) (no basis). Space Θ(V) (forgets
  that the adjacency lists hold E entries).
- **Probe questions:** "Which inputs are fast for this code even with `pop(0)`?" → those where
  `ready` stays short, e.g. a single long chain a→b→c→…: Θ(V + E). "Is `ready.pop()` (from the end) a
  fix?" → yes for complexity, Θ(V + E). It's still a valid topological order (any ready node may go
  next); only the tie-breaking changes from FIFO to LIFO.
- **Variant seeds:** BFS shortest path with `queue.pop(0)` on a star graph (Θ(V²)); course-schedule
  with `ready.insert(0, t)` instead of append.
- **Verified:** derivation ×2 + empirical op-count (E = 0: vary V → V²; dense DAG with V fixed, vary
  E → E) + timing of one `list.pop(0)` vs list length (linear). Whole-function timing for E = 0
  grows like V² with an extra memory-hierarchy bump past ~32K items (best fit n²log n by
  spread), recorded as info only.
- **Retired:** —

## IV-19
- **Trick:** catalan-backtracking
- **Secondary tricks:** str-concat, stack-depth-vs-total-calls
- **Source:** LeetCode generate-parentheses
- **Hidden inefficiency:** none
- **Difficulty:** 3/3
- **Time:** Θ(4ⁿ/√n), equivalently Θ(n·C_n), where C_n = C(2n, n)/(n+1) ≈ 4ⁿ/(√π·n^{3/2}) is the
  number of results. **Accepted tight forms:** Θ(4ⁿ/√n) or Θ(n·C_n) → Pass. **Partial**
  (valid but loose): O(4ⁿ), O(2^{2n}), O(n·4ⁿ). **Miss:** Θ(C_n) or Θ(4ⁿ/n^{1.5}) (drops the cost
  of building each length-2n string), O(2ⁿ), O(n!), O(n²).
- **Space:** Θ(n²) auxiliary: 2n+1 active frames, and the frame at depth d holds its own `cur` of
  length d, so 0 + 1 + … + 2n. The output (C_n strings of length 2n, Θ(4ⁿ/√n)) is not counted.
- **Why:** The recursion tree only contains valid prefixes. The number of tree nodes is Θ(C_n)
  (verified: nodes/C_n → ≈ 5), because most nodes sit near full length and every one of them
  extends to at least one leaf. Each node builds `cur + "("` or `cur + ")"`, a fresh string copy of
  O(n). So the total is Θ(n·C_n) = Θ(4ⁿ/√n), and the C_n leaves alone already cost 2n·C_n to
  produce. Space: `cur` is immutable and every call makes a new one, so the strings along the
  current path add up to Θ(n²).
- **Common wrong answers:** Θ(2^{2n}) = Θ(4ⁿ) — Partial (a loose "two choices per position" bound;
  the ballot constraint cuts it by a polynomial factor). Θ(C_n) — Miss (forgets the per-string
  copy). Θ(n·2ⁿ) — Miss (counts only n levels of choices, but the depth is 2n). Space Θ(n) —
  Miss (counts only frames, not the string each frame holds). Space Θ(4ⁿ/√n) — Pass only if the
  learner explicitly says they're counting the output.
- **Probe questions:** "Roughly how many strings for n = 10, and how many characters in total?" →
  C_10 = 16,796 strings of 20 chars ≈ 3.4×10⁵ chars. "What if `cur` were a shared list with
  append/pop and `''.join(cur)` only at the leaves?" → still Θ(n·C_n) time (the leaf joins dominate),
  but Θ(n) auxiliary space.
- **Variant seeds:** all binary strings of length n with no two adjacent 1s (Fibonacci count ×n); all
  valid IP-address splits (bounded fan-out — constant work).
- **Verified:** derivation ×2 + empirical op-count (chars copied + calls fit 4ⁿ/√n over n = 4…13,
  ahead of 4ⁿ and 4ⁿ/n^{1.5}; peak chars held by live frames fit n²)
- **Retired:** —

## IV-20
- **Trick:** dijkstra-lazy-heap
- **Secondary tricks:** multi-variable-bound
- **Source:** LeetCode network-delay-time
- **Hidden inefficiency:** none
- **Difficulty:** 2/3
- **Time:** Θ(E log V), which is the same as Θ(E log E) since E ≤ V². The standard answer
  Θ((V + E) log V) also Passes. The code itself does no Θ(V) work, because only reached nodes ever
  enter `dist`.
- **Space:** Θ(E) (`graph` stores E edges, the heap holds ≤ E + 1 entries including stale
  duplicates, `dist` ≤ min(V, E + 1)). Θ(V + E) also Passes.
- **Why:** Each node is finalized once, the first time it's popped. When u is finalized, each
  outgoing edge pushes at most one entry, so there are ≤ E + 1 pushes, and therefore ≤ E + 1 pops,
  stale entries included. Every heap operation is O(log(heap size)) = O(log E) = O(log V). On dense
  graphs the heap really does grow to Θ(E) (verified on complete graphs), so the log factor is real.
- **Common wrong answers:** Θ(V²) (array-based Dijkstra — not this code). Θ(V log V) (forgets the
  E pushes and the stale duplicates). Θ(V·E) (Bellman–Ford). Space Θ(V) (forgets that the heap can
  hold one entry per edge, and the adjacency lists).
- **Probe questions:** "What breaks if you delete `if u in dist: continue`?" → correctness: a stale,
  larger distance overwrites `dist[u]`. Complexity: u's edges are re-scanned on every stale pop, so
  the "each edge pushes once" argument (and the E + 1 heap bound) fails. "When is
  array-based O(V²) Dijkstra better?" → dense graphs (E ≈ V²): V² beats V² log V.
- **Variant seeds:** cheapest flights within k stops (state = (node, stops), V·k states); path with
  minimum effort on a grid (V = m·n, E ≈ 4mn → Θ(mn log(mn))).
- **Verified:** derivation ×2 + empirical op-count (heap comparisons counted: complete graph vs V →
  V² log V; sparse E = 4V → V log V; heap peak on complete graph → V²)
- **Retired:** —
