# Keys — amortized_multivar.py (tutor only — learner does not open)

Conventions for this file: SPACE is auxiliary. The input is excluded. A structure the function
builds and returns (a buffer, a trie, groups) counts, because the function allocated it. Dict/set
operations are expected O(1) plus the cost of hashing the key. Where a bound is usually written
either as O(E log V) or O(E log E), both are accepted (log E ≤ 2 log V). For union-find,
"α(n), effectively constant" is the expected wording. Answering O(1) per op with no mention of α
is Partial: probe once.

## AM-01
- **Trick:** two-stack-queue
- **Difficulty:** 2/3
- **Time:** Θ(n)
- **Space:** Θ(n)
- **Single-op:** Θ(n)
- **Why:** Aggregate argument: each job is appended to `incoming` once, moved to `outgoing` at
  most once (the `while` loop), and popped once. That is ≤ 3 unit moves per job over the whole run,
  so all `while` iterations together cost ≤ n. Total is Θ(n), O(1) amortized per command. One
  `print` that arrives while `outgoing` is empty and n−1 jobs sit in `incoming` moves all of them,
  so a single command costs Θ(n).
- **Common wrong answers:** Θ(n²) for TIME (sees the `while` inside the `for` and charges n per
  print. The transfer only happens when `outgoing` is empty, and each job can be transferred only
  once); Θ(1) for SINGLE-OP (confuses amortized with worst single op); Θ(n) for TIME with
  "because each op is O(1)" (right bound, wrong reason: no single op is O(1) worst case. Partial,
  so probe).
- **Probe questions:** "Give an input where one print costs n." → n−1 jobs, then a print.
  "Why can't that happen on every print?" → after the transfer `outgoing` holds n−1 jobs, so the
  next n−2 prints transfer nothing. Each job moves once (accounting: charge 2 extra coins at push
  time).
- **Variant seeds:** a buggy version that moves `outgoing` back into `incoming` after every print
  (Θ(n²), so amortization breaks); a "min-queue" built from two stacks that each hold
  (value, running_min) pairs.
- **Verified:** derivation ×2 + empirical op-count
- **Retired:** —

## AM-02
- **Trick:** word-search-backtracking
- **Difficulty:** 3/3
- **Time:** O(m·n·3ᴸ)
- **Space:** Θ(L)
- **Why:** Up to m·n starting cells. From a start, the first step branches 4 ways. Every later
  step branches at most 3 ways, because the cell you came from is marked `"#"` and fails at once.
  So one start explores ≤ 4·3ᴸ⁻¹ paths, giving m·n·4·3ᴸ⁻¹ = O(m·n·3ᴸ) calls with O(1) work each.
  Worst case: a board of all `"A"` with word `"AA…AB"`, so nothing ever matches. Recursion depth is
  ≤ L+1, and the board is changed in place, so space is Θ(L) (Θ(min(L, m·n)) if L could exceed
  the board).
- **Note on tightness:** O(m·n·3ᴸ) is the standard interview answer and the expected one. Strictly,
  self-avoiding walks on a grid grow like ~2.64ᴸ, not 3ᴸ (the empirical growth ratio fell from
  3.1 to 2.64 for L = 4…9), so 3ᴸ is a safe upper bound and not a literal Θ. Do not penalize the
  learner for using 3ᴸ. O(m·n·4ᴸ) is valid but loose, so Partial: probe on why one branch dies.
- **Common wrong answers:** O(m·n·L) (treats it as a linear scan from each cell and forgets the
  branching); O(4ᴸ) (forgets the m·n starting cells); O((m·n)²) (thinks of it as a DFS per cell
  bounded by board size); Space O(m·n) (assumes a visited set copy. Marking is in place, and the
  stack depth is L).
- **Probe questions:** "Why 3 and not 4 after the first step?" → the neighbor you came from is
  marked `"#"`, so that branch returns immediately. "What if the code kept a `visited` set and
  passed `visited | {(r, c)}` down?" → each call copies up to L items, so time is O(m·n·3ᴸ·L) and
  space is O(L²).
- **Variant seeds:** search for every word in a list of w words separately (O(w·m·n·3ᴸ)), compared
  with a trie-guided search; allow 8-directional moves (O(m·n·7ᴸ)).
- **Verified:** derivation ×2 + empirical op-count (m·n factor fitted linearly. 3ᴸ checked as an
  upper bound, observed base ≈ 2.64)
- **Retired:** —

## AM-03
- **Trick:** trie-total-chars
- **Difficulty:** 1/3
- **Time:** Θ(S)
- **Space:** Θ(S)
- **Why:** Each character of each word costs one O(1) dict lookup and maybe one insert, so the
  time is Σ len(w) = S. In the worst case no two words share a prefix, every character creates a
  new node, and there are S nodes.
- **Common wrong answers:** O(n·k) where k is the max length (valid but loose when lengths
  differ: Partial. Probe: "words of lengths 1, 1, …, 1, 10⁶?"); O(S²) or O(n²) (thinks the
  `ch not in node` check scans something. It is a dict lookup); O(26·S) as distinct from O(S)
  (an alphabet factor only applies to array-of-26 children, and it is still Θ(S) for a fixed
  alphabet); Space O(n) (counts words, not nodes).
- **Probe questions:** "When is the space much smaller than S?" → when words share long prefixes,
  e.g. "a", "ab", "abc", … share every node. "Doing the same with a Python set of every prefix
  `w[:i]` instead?" → each slice costs O(i), so Θ(Σ len(w)²), which can be Θ(n·k²).
- **Variant seeds:** an autocomplete that walks to a prefix node and then collects every word below
  it (output-sensitive: O(p + size of subtree)); a trie with 26-slot list children (space
  Θ(26·S) = Θ(S·Σ) if the alphabet size is kept as a variable).
- **Verified:** derivation ×2 + empirical op-count
- **Retired:** —

## AM-04
- **Trick:** union-find
- **Difficulty:** 2/3
- **Time:** Θ(n + m·α(n))
- **Space:** Θ(n)
- **Single-op:** Θ(log n)
- **Why:** Building `parent` and `rank` costs Θ(n). With union by rank plus path compression, any
  sequence of m finds/unions costs O(m·α(n)) in total. This is the Tarjan amortized bound, proved
  with a potential argument. α is the inverse Ackermann function, ≤ 4 for any realistic n. For a
  single find, union by rank alone keeps tree height ≤ log₂ n (a root of rank r has ≥ 2ʳ nodes),
  and that height is reachable. Pair up roots level by level, (0,1), (2,3), (0,2), …, to build a
  binomial tree, then call find on its deepest leaf for Θ(log n) before compression flattens it.
  The find recursion depth is ≤ log n, which fits inside Θ(n).
- **Common wrong answers:** O(m log n) for TIME (rank only: a valid but loose bound, so Partial);
  O(m·n) (thinks of naive union-find without rank or compression); O(1) for SINGLE-OP (amortized
  is not worst case: one find can climb log n levels); O(m) with no init term (Partial if n ≫ m
  matters: `list(range(n))` is Θ(n)).
- **Probe questions:** "Remove `rank` and keep path compression. Total?" → O(n + m log n)
  amortized (Tarjan–van Leeuwen), which is still good. "Remove both?" → chains of length n, Θ(m·n)
  (see AM-11). "Why is one find at most log n?" → by the rank ⇒ size ≥ 2^rank argument.
- **Variant seeds:** an "accounts merge" disguise where emails are keyed through a dict (adds
  hashing O(len email) per lookup); union by size instead of rank, with an iterative two-pass
  find.
- **Verified:** derivation ×2 + empirical op-count (total linear at m = 4n. Single find fits
  log n on a binomial-tree construction)
- **Retired:** —

## AM-05
- **Trick:** adjacency-list-vs-matrix
- **Difficulty:** 2/3
- **Time:** Θ(V + E)
- **Space:** Θ(V + E)
- **Why:** Building the lists costs Θ(V) to allocate plus Θ(E) appends. In the `while` loop each
  step is dequeued at most once (Θ(V)), and the inner `for` walks `unlocks[s]` once for that s.
  Summed over all s, those lists hold exactly E entries, so all inner iterations total E. That is
  an aggregate count of edges, not "V iterations × E each". Space: lists hold V + E entries, plus
  the Θ(V) counters, queue, and order.
- **Common wrong answers:** O(V·E) (multiplies the `while` by the worst inner list size. Each
  edge is touched once in total); O(V²) (assumes a matrix, or that every step scans every
  other step); O(V) (forgets the edge work); O(E) only (forgets the Θ(V) init and queue: Partial
  if the graph can have isolated steps).
- **Probe questions:** "If `must_precede` were given as a V×V boolean matrix and you scanned row s
  instead of `unlocks[s]`?" → Θ(V²) regardless of E. "What does `len(order) != V` detect?" → a
  cycle, which does not change the bound.
- **Variant seeds:** DFS-based topological sort with a recursion stack (same Θ(V+E), recursion
  depth up to V); counting reachable nodes from *every* node with a BFS each (Θ(V·(V+E))).
- **Verified:** derivation ×2 + empirical op-count
- **Retired:** —

## AM-06
- **Trick:** dynamic-array-amortized
- **Difficulty:** 3/3
- **Time:** Θ(n²/k)
- **Space:** Θ(n)
- **Why:** Aggregate argument: a resize happens at sizes 0, k, 2k, …, and resize j allocates
  (j+1)·k slots and copies j·k items. Over the run that is about k·(1 + 2 + … + n/k) ≈ n²/(2k) for
  allocation plus the same for copying, plus n writes. Since k ≤ n, n²/k ≥ n, so Θ(n²/k). That is
  Θ(n/k) amortized per add, and with a constant chunk it is Θ(n²) overall, Θ(n) per add. Space:
  capacity < n + k ≤ 2n, and old plus new blocks coexist during a copy, so still Θ(n).
- **Common wrong answers:** Θ(n) or "amortized O(1)" (assumes every dynamic array is O(1)
  amortized. That needs *geometric* growth, and adding a constant chunk gives an arithmetic
  series); Θ(n²) (drops k. That is a Miss under "keep every variable that matters". Accept it only
  if the learner says "for constant k" and gives n²/k when probed); Θ(n·k) (multiplies instead
  of dividing); Θ(n/k) for TIME (that is the per-add amortized cost, not the total).
- **Probe questions:** "What if k = √n?" → Θ(n^1.5). "What if the line were
  `self.cap = 2 * self.cap + self.chunk`?" → geometric, Θ(n) total, O(1) amortized.
- **Variant seeds:** growth `cap = cap + int(cap ** 0.5) + 1` (√-growth: Θ(n^1.5)); a shrink rule
  (halve when half-empty) driven by alternating push/pop at the boundary (thrashing: Θ(n) per op).
- **Verified:** derivation ×2 + empirical op-count (k fixed → n²; k = √n → n^1.5; n fixed → 1/k)
- **Retired:** —

## AM-07
- **Trick:** top-k-heap
- **Difficulty:** 1/3
- **Time:** Θ(n log k)
- **Space:** Θ(k)
- **Why:** The heap never holds more than k items, so every push or replace costs O(log k). In the
  worst case (strictly increasing scores) all n − k later scores trigger `heapreplace`, sifting
  down Θ(log k) levels. The final `sorted` costs k log k ≤ n log k. Read as Θ(n·(1 + log k)), it
  covers the k = 1 case.
- **Common wrong answers:** O(n log n) (thinks the heap grows to n. It is capped at k: Partial,
  since it is valid but loose. Probe with k = 10, n = 10⁹); O(n·k) (thinks `heapreplace` scans
  the heap); O(k log n) (swaps the roles); Space O(n) (same heap-size misconception).
- **Probe questions:** "Which input forces a replace on every element?" → increasing scores.
  "Alternative: `heapq.heapify(scores)` then pop k times?" → O(n + k log n) time, but O(n) space
  if you copy the input.
- **Variant seeds:** the k closest points to the origin using a max-heap via negated distances
  (still n log k); a merge of k sorted lists of total length N (O(N log k)).
- **Verified:** derivation ×2 + empirical op-count (n varies → n; k varies → n log k; k = n/4 →
  n log n)
- **Retired:** —

## AM-08
- **Trick:** dijkstra-lazy-heap
- **Difficulty:** 3/3
- **Time:** Θ((V + E) log V)
- **Space:** Θ(V + E)
- **Why:** Each vertex is settled once, and its edges are relaxed once, so Θ(E) relaxations total.
  Each successful relaxation pushes a new entry. Old ones are not removed ("lazy deletion"), so the
  heap can hold up to E + 1 entries, and each push/pop costs O(log E) = O(log V). Stale pops are
  skipped by the `settled` check, but each was paid for by one push. Total O((V + E) log V). Space:
  `best` and `settled` are Θ(V) and the heap holds up to Θ(E) stale entries. This is tight on an
  adversarial dense DAG where every relaxation improves the distance.
- **Accepted forms:** O(E log V), O(E log E), O((V+E) log E). V, E refer to the part reachable
  from `home`.
- **Common wrong answers:** O(V log V) (forgets that edges cause pushes); O(V²) (that is the
  array-based Dijkstra); O(V·E) (Bellman–Ford thinking, or "the `for` runs E times inside a
  `while` that runs V times"); Space Θ(V) (assumes decrease-key. Lazy deletion keeps duplicates,
  up to Θ(E)); O(E log E) is fine and is not a mistake.
- **Probe questions:** "Why is log E the same as log V here?" → E ≤ V², so log E ≤ 2 log V.
  "Remove `if u in settled: continue`. Still correct? Cost?" → still correct (a stale entry's
  relaxations never improve anything), but each stale pop rescans u's edges. Work becomes Σᵤ indeg(u)·outdeg(u),
  up to Θ(V³) on a dense graph.
- **Variant seeds:** a grid-of-weights shortest path (V = m·n, E ≈ 4mn → O(mn log(mn))); a
  Dijkstra that keys the heap on (time, stops) with up to K stops, giving state space V·K.
- **Verified:** derivation ×2 + empirical op-count (dense adversarial DAG: count fits
  (V+E) log V, peak heap size fits E ≈ V²/2)
- **Retired:** —

## AM-09
- **Trick:** monotonic-stack
- **Difficulty:** 2/3
- **Time:** Θ(n)
- **Space:** Θ(n)
- **Why:** Accounting argument: every index is pushed exactly once (one `append` per `for` step)
  and can be popped at most once. So the total `while` iterations over the whole run are ≤ n + 1,
  even though a single step may pop Θ(n) (the trailing 0 flushes an increasing stack). `heights +
  [0]` is a Θ(n) copy. The stack can hold n + 1 entries (increasing heights).
- **Common wrong answers:** O(n²) (sees the `while` inside the `for`, and the worst single step
  is n pops, but that cannot happen at every step); O(n log n) (vague "stack makes it log");
  Space O(1) (forgets both the stack and the `heights + [0]` copy).
- **Probe questions:** "Which input makes one iteration pop everything?" → strictly increasing
  heights, where the sentinel 0 pops all n. "Why can't every step do that?" → once popped, an
  index is gone, and there are only n pushes to pay for pops.
- **Variant seeds:** "daily temperatures" (next greater element to the right) written with a
  `for` over reversed indices; sliding-window maximum with a monotonic deque (Θ(n), not Θ(n·w)).
- **Verified:** derivation ×2 + empirical op-count
- **Retired:** —

## AM-10
- **Trick:** grid-bfs
- **Difficulty:** 1/3
- **Time:** Θ(m·n)
- **Space:** Θ(m·n)
- **Why:** The double `for` visits m·n cells once each. A cell enters `seen` and the queue at most
  once across all BFS runs, because `seen` is shared, and each dequeued cell checks 4 neighbors. So
  all the BFS work together is O(4·m·n). Tuple keys have size 2, so hashing is O(1). `seen` can
  hold every cell (all land), so space is Θ(m·n).
- **Common wrong answers:** O((m·n)²) (thinks "a BFS of up to m·n cells, started from each of m·n
  cells". `seen` makes later starts skip immediately); O(m·n·k) for k islands (each island's BFS
  only touches its own cells); Space O(m + n) (that bounds the BFS *frontier*, but `seen` holds
  every land cell).
- **Probe questions:** "What if `seen` were reset to `set()` at the start of each BFS?" → the outer
  `not in seen` check stops working, so every land cell starts its own BFS. The count is wrong,
  and an all-land grid costs O((m·n)²).
  "Replace `seen` by overwriting `grid[r][c] = '.'`?" → time is the same, auxiliary space drops to
  the queue size.
- **Variant seeds:** a multi-source BFS from every "gate" at once (still Θ(m·n), not
  Θ(gates·m·n)); a BFS whose state is (r, c, keys_bitmask) with K keys (Θ(m·n·2ᴷ)).
- **Verified:** derivation ×2 + empirical op-count
- **Retired:** —

## AM-11
- **Trick:** union-find
- **Difficulty:** 3/3
- **Time:** Θ(m·n)
- **Space:** Θ(n)
- **Why:** Neither rank nor path compression is used, so a tree can become a chain. Pairs
  (0,1), (1,2), …, (n−2, n−1) build 0→1→…→n−1 cheaply, because each `top(a)` starts at a root.
  After that, every remaining pair such as (0, n−1) walks the full chain: Θ(n) per pair, Θ(m·n)
  total. The final set comprehension adds up to Θ(n²) ≤ Θ(m·n) since m ≥ n. Without the m ≥ n
  assumption the bound is Θ(n + m·min(m, n)). Space: `boss` and the set of tops are Θ(n).
- **Common wrong answers:** O(m·α(n)) or O(m log n) (assumes the optimized union-find. Nothing
  here bounds tree height); O(m) or O(n + m) (assumes `top` is O(1)); O(n²) (sees only the final
  comprehension, which is a Miss because the m factor is dropped).
- **Probe questions:** "Smallest change that brings it to O(log n) per find?" → union by size/rank,
  i.e. attach the smaller tree under the larger. "Add only `boss[x] = boss[boss[x]]` inside the
  loop (path halving)?" → O(log n) amortized per op even without rank.
- **Variant seeds:** a "friend circles" adjacency-matrix version that calls union for every 1 in
  an n×n matrix with naive finds (O(n³) worst); union-by-rank but no compression (O(m log n),
  tight).
- **Verified:** derivation ×2 + empirical op-count (m = 2n → n²; n fixed, m varies → m)
- **Retired:** —

## AM-12
- **Trick:** dynamic-array-amortized
- **Difficulty:** 2/3
- **Time:** Θ(n)
- **Space:** Θ(n)
- **Single-op:** Θ(n)
- **Why:** Aggregate argument: capacities grow by a factor of at least 1.5 (1, 2, 4, 7, 11, 17,
  26, …). The total allocated plus copied cells is a geometric series bounded by
  cap_final·(1 + 2/3 + 4/9 + …) = 3·cap_final ≤ 3(1.5n + 1), which is Θ(n), so O(1) amortized
  per push. (An accounting argument also works: charge each push a constant number of
  coins, about 1 + 3, and each resize is prepaid by the pushes since the previous one.) A single push that
  lands on a full buffer copies `size` ≈ n items and allocates ≈ 1.5n, so Θ(n). Space: capacity
  ≤ 1.5n + 1, and old plus new coexist during a copy, so Θ(n).
- **Common wrong answers:** Θ(n log n) (charges log n resizes × n each instead of summing the
  geometric series); Θ(n²) (charges a full copy on every push); "only doubling is amortized O(1)"
  (any constant factor > 1 works, and only the constant changes); Θ(1) for SINGLE-OP (amortized
  is not worst case); Θ(log n) for SINGLE-OP (confuses it with the number of resizes so far).
- **Probe questions:** "How many resizes happen in n pushes?" → Θ(log n) (base 1.5), which is a
  count, not a cost. "Change the growth to `cap + 100`?" → arithmetic growth, Θ(n²) total (see
  AM-06).
- **Variant seeds:** a buffer that doubles on push and halves when a quarter-full on pop (still
  O(1) amortized, unlike halving at half-full); a ring buffer that doubles and has to "unwrap"
  the elements on resize.
- **Verified:** derivation ×2 + empirical op-count (total → n; single push measured at n = cap+1
  → n)
- **Retired:** —

## AM-13
- **Trick:** adjacency-list-vs-matrix
- **Difficulty:** 3/3
- **Time:** Θ(V²)
- **Space:** Θ(V + E)
- **Why:** The conversion comprehension looks at every matrix cell, V·V checks, no matter how
  sparse the graph is. The DFS that follows is Θ(V + E) because each vertex is pushed once and
  each list entry is scanned once, and E ≤ V² so it is absorbed. Under the stated sparsity
  (E ≈ V) the space is Θ(V): `nbrs` holds V + E entries, plus `seen` and the stack at Θ(V).
- **Accepted forms:** Space Θ(V + E) or Θ(V) (given sparsity). Time must be Θ(V²). The input
  representation forces reading every cell.
- **Common wrong answers:** Θ(V + E) or Θ(V) for TIME (sees an adjacency-list DFS and forgets that
  building the list scanned the whole matrix. The "sparse" comment is bait); Θ(V·E) (multiplies
  vertices by edges); Space Θ(V²) (thinks the lists are as big as the matrix. They only store the
  1s).
- **Probe questions:** "Is there any way to beat V² given only this matrix?" → no. Any correct
  algorithm must be able to inspect each cell, since an unread cell could hide an edge. "What if
  the input were already an adjacency list?" → Θ(V + E).
- **Variant seeds:** count connected components by DFS directly over matrix rows (Θ(V²));
  convert an edge list into a V×V matrix "for O(1) edge lookups" and then BFS (Θ(V²) time and
  space even when E ≈ V).
- **Verified:** derivation ×2 + empirical op-count (path graph, E ≈ V → V²)
- **Retired:** —

## AM-14
- **Trick:** anagram-grouping
- **Difficulty:** 1/3
- **Time:** Θ(n·k log k)
- **Space:** Θ(n·k)
- **Why:** For each of the n plates, `sorted(p)` costs Θ(k log k), and `"".join` and hashing the
  signature cost Θ(k), which is dominated. The final list comprehension is Θ(n). In the worst case
  all signatures are distinct, so the dict stores n signature strings of length up to k, Θ(n·k)
  characters. The grouped lists hold references, Θ(n).
- **Common wrong answers:** O(n log n) (thinks it sorts the list of plates rather than each
  plate's characters); O(n·k) (forgets that the per-string sort is k log k. That would be correct
  for a 26-count signature); O(n²·k) (thinks it compares every pair of plates); Space O(n)
  (forgets the signatures are new strings of length k).
- **Probe questions:** "How do you get O(n·k)?" → use a 26-slot count tuple (or a counting sort)
  as the key, which costs O(k + 26) per plate. "Does hashing a length-k string cost O(1)?" → no, it
  costs O(k) the first time, but it is dominated here.
- **Variant seeds:** group by `tuple(sorted(Counter(p).items()))` (O(k + d log d), where d is the
  number of distinct characters); group strings by "shift pattern" (each char minus the first,
  mod 26: O(n·k)).
- **Verified:** derivation ×2 + empirical op-count (n varies, k fixed → n; k varies → k log k)
- **Retired:** —

## AM-15
- **Trick:** binary-search-on-answer
- **Difficulty:** 2/3
- **Time:** Θ(n·log(n·W)) = Θ(n log n + n log W)
- **Space:** Θ(1)
- **Why:** The search range is [max, sum], whose width is at most sum ≤ n·W. That gives
  log₂(n·W) halvings, and each one runs `fits`, a Θ(n) scan. The initial `max` and `sum` cost
  Θ(n). The bound is tight with all weights equal to W, where the range is (n−1)·W. Only a few
  scalars are used.
- **Accepted forms:** Θ(n log S) where S = sum(weights) is Partial. Probe: "express it in n and
  W", which gives S ≤ nW. Θ(n·log(nW)) and Θ(n(log n + log W)) are Pass.
- **Common wrong answers:** O(n log n) (pattern-matches "binary search", but the range is values,
  not indices, and W matters); O(n log W) (drops the log n term. With all weights 1, W = 1 but
  it still takes log n rounds: Miss); O(n·S) or O(n·nW) (thinks of a linear scan over every
  capacity); O(log(nW)) (forgets that each probe is a Θ(n) feasibility check).
- **Probe questions:** "Why is `fits` monotone, and why does that matter?" → a larger capacity
  never needs more trucks, which is what makes binary search valid. "If weights were sorted and you
  used prefix sums plus bisect inside `fits`, stopping once trucks exceed `days`?" → each check
  costs O(days·log n), so the total is O(n + days·log n·log(nW)).
- **Variant seeds:** "Koko eating bananas" with h hours, using `ceil(p / speed)` per pile
  (Θ(n log P), P = max pile); the minimum largest subarray sum when splitting into d parts
  (identical structure, range [max, sum]).
- **Verified:** derivation ×2 + empirical op-count (n varies, W fixed → n log(nW); W varies, n
  fixed → log(nW); random weights → n log(nW))
- **Retired:** —
