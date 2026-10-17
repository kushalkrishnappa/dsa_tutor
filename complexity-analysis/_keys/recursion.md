# Keys — recursion.py (tutor only — learner does not open)

## RR-01
- **Trick:** halving-with-linear-work
- **Difficulty:** 2/3
- **Time:** Θ(n)
- **Space:** Θ(n)
- **Why:** T(n) = T(n/2) + Θ(n). Round work is n/2 + n/4 + … < n, so Θ(n) total (equivalently: every
  `stronger()` call eliminates one player, so there are exactly n − 1 matches). Space: each frame keeps
  its `next_round` list alive while it waits on the recursive call, so n/2 + n/4 + … = Θ(n) live
  elements, plus Θ(log n) frames.
- **Common wrong answers:** Θ(n log n) time (log n rounds × n per round — forgets rounds shrink
  geometrically); Θ(log n) space (counts only stack depth, misses the list each frame holds); Θ(1) space
  ("no extra data structure").
- **Probe questions:** "Exactly how many times is `stronger()` called?" → n − 1; each match knocks out
  one player. "How would you make the auxiliary space Θ(1)?" → write winners back into a prefix of
  `players` and loop over a shrinking length (mutates the input).
- **Variant seeds:** recursive pairwise-sum reduction (`sums of adjacent pairs` until one value);
  keep only the elements above the median of a 3-way partition and recurse on `n // 3` (T(n/3)+n).
- **Verified:** derivation ×2 + empirical op-count
- **Retired:** —

## RR-02
- **Trick:** stack-depth-vs-total-calls
- **Difficulty:** 1/3
- **Time:** Θ(n)
- **Space:** Θ(n)
- **Why:** T(n) = T(n − 1) + O(1) → Θ(n). The call is in tail position, but CPython does not eliminate
  tail calls, so all n + 1 frames are on the stack when the base case is reached → Θ(n) space.
- **Common wrong answers:** Θ(1) space ("it's tail-recursive, so it's a loop" — true in Scheme or with
  some C compilers, not in CPython); Θ(1) space because only one integer accumulator exists (forgets
  that each frame is memory).
- **Probe questions:** "What happens on a 10,000-node list with default settings?" → `RecursionError`
  (default limit ≈ 1000 frames). "Rewrite for Θ(1) space?" → a `while node:` loop.
- **Variant seeds:** tail-recursive countdown sum `drain(k, acc)`; tail-recursive binary search
  (`return search(lo, mid - 1)`) — Θ(log n) space, not Θ(1).
- **Verified:** derivation ×2 + empirical op-count
- **Retired:** —

## RR-03
- **Trick:** uneven-split-recurrence
- **Difficulty:** 3/3
- **Time:** Θ(n log n)
- **Space:** Θ(log n)
- **Why:** T(n) = T(n/3) + T(2n/3) + Θ(n). Recursion tree: every level's sizes add to ≤ n (exactly n
  until the n/3-branch bottoms out at depth log₃ n); depth is log_{3/2} n. So the total is between
  n·log₃ n and n·log_{3/2} n → Θ(n log n). Space = longest root-to-leaf path (always taking the 2/3
  side) = log_{3/2} n frames → Θ(log n).
- **Common wrong answers:** Θ(n) ("1/3 + 2/3 = 1, so it's like one call" or a bad Master-Theorem fit);
  Θ(n^{log_{3/2} 2}) ≈ n^1.71 (treats it as 2T(2n/3) + n); Θ(n) space (assumes the 2n/3 chain is linear
  in length, or confuses space with time).
- **Probe questions:** "Why can't you plug this into the Master Theorem?" → subproblems have unequal
  sizes; use a recursion tree (or Akra–Bazzi: (1/3)^p + (2/3)^p = 1 gives p = 1 → Θ(n log n)). "What if
  the cut were at 1/10 instead of 1/3?" → still Θ(n log n); only the log base changes.
- **Variant seeds:** split at 1/4 and 3/4 with a linear scan; T(n/3) + T(n/2) + n (fractions sum < 1) →
  Θ(n) — tests whether the learner checks the fraction sum.
- **Verified:** derivation ×2 + empirical op-count
- **Retired:** —

## RR-04
- **Trick:** subsets-enumeration
- **Difficulty:** 2/3
- **Time:** Θ(n·2ⁿ)
- **Space:** Θ(n)
- **Why:** Include/exclude recursion: 2^{n+1} − 1 calls of O(1) plus 2ⁿ leaves, each calling
  `score(chosen)` in O(|chosen|); Σ over all subsets of |S| = n·2^{n−1} → Θ(n·2ⁿ). Space: only one
  `chosen` path (≤ n items) and n + 1 frames exist at any moment → Θ(n).
- **Common wrong answers:** Θ(2ⁿ) time (forgets the leaf cost of `score`); Θ(n·2ⁿ) or Θ(2ⁿ) space
  (thinks every subset is stored, or counts total calls instead of the live path — append/pop reuses
  one list).
- **Probe questions:** "If each leaf did `results.append(list(chosen))`?" → space Θ(n·2ⁿ) for the
  output. "If `score` were O(1)?" → Θ(2ⁿ) time.
- **Variant seeds:** bitmask loop `for mask in range(1 << n)` with an O(popcount) evaluation;
  include/exclude with a size cap k (pruned when len(chosen) == k → Σ C(n, i) leaves).
- **Verified:** derivation ×2 + empirical op-count
- **Retired:** —

## RR-05
- **Trick:** memoization-collapse
- **Difficulty:** 1/3
- **Time:** Θ(n)
- **Space:** Θ(n)
- **Second call:** Θ(1)
- **Why:** T(n) = T(n − 1) + O(1) once memoized: the `rr05(n - 1)` branch fills the memo for every
  smaller value, so `rr05(n - 2)` is always a hit → ≤ 2n calls. Space: memo holds n − 1 entries and the
  first branch descends n → 1 before anything is cached, so depth is Θ(n) too. The memo is
  module-level, so an immediate second `rr05(n)` returns from the dict in O(1).
- **Common wrong answers:** Θ(2ⁿ) or Θ(φⁿ) time (ignores the memo); Θ(1) space (counts only the
  answer, forgets memo and stack); second call Θ(n) (assumes the cache resets per call).
- **Probe questions:** "After rr05(n), what does rr05(2n) cost?" → Θ(n): only n new states. "Swap the
  order so `rr05(n - 2)` is evaluated first — still Θ(n) time and space?" → yes; depth becomes ~n/2 on
  the first descent but the memo is still Θ(n).
- **Variant seeds:** same code with `@lru_cache` on an inner function created per call (second call
  Θ(n)); memoized tribonacci-style "min cost with 1, 2, or 3 steps".
- **Verified:** derivation ×2 + empirical op-count
- **Retired:** —

## RR-06
- **Trick:** master-theorem-root-heavy
- **Difficulty:** 3/3
- **Time:** Θ(n²)
- **Space:** Θ(log n)
- **Why:** T(n) = 3T(n/2) + Θ(n²) (three overlapping halves, all-pairs loop). n^{log₂ 3} ≈ n^1.585 <
  n², and 3·(n/2)² = ¾·n² (regularity holds) → Master case 3 → Θ(n²). Recursion tree: level i costs
  (n²/2)·(3/4)^i, a decreasing geometric series dominated by the root. Space: depth log₂ n, O(1) per
  frame → Θ(log n).
- **Common wrong answers:** Θ(n² log n) (assumes each of log n levels costs n² — forgets level cost
  shrinks by 3/4); Θ(n^{log₂ 3}) (assumes the branching factor always dominates); Θ(n²) or Θ(n) space
  (confuses work with live memory).
- **Probe questions:** "What if there were 4 recursive calls on halves?" → 4T(n/2) + n², case 2 →
  Θ(n² log n). "5 calls?" → case 1 → Θ(n^{log₂ 5}) ≈ n^2.32.
- **Variant seeds:** 2T(n/2) + n² disguised as a pairwise-conflict check per segment; 7T(n/2) + n³ →
  Θ(n³).
- **Verified:** derivation ×2 + empirical op-count
- **Retired:** —

## RR-07
- **Trick:** fibonacci-branching
- **Difficulty:** 2/3
- **Time:** Θ(φⁿ) (φ ≈ 1.618)
- **Space:** Θ(n)
- **Why:** Let A(r) = calls from `count(r, False)`, B(r) from `count(r, True)`. A(r) = 1 + A(r−1) + B(r−1),
  B(r) = 1 + A(r−1) → A(r) = A(r−1) + A(r−2) + 2: Fibonacci growth → Θ(φⁿ). (Cross-check: each leaf
  returns 1, so leaves = the answer = F(n+2) ≈ φ^{n+2}/√5.) Space: depth n + 1 frames → Θ(n).
- **Common wrong answers:** O(2ⁿ) (two branches per call — a valid but loose bound: Partial; after a 1
  only one branch exists); Θ(n) time (sees one decreasing parameter); Θ(φⁿ) or Θ(2ⁿ) space (counts
  total calls instead of the deepest path).
- **Probe questions:** "Why isn't it 2ⁿ?" → the `last_was_one=True` calls have one child, so the tree
  is Fibonacci-shaped: leaves = number of valid codes ≈ 1.618ⁿ. "Make it Θ(n)?" → memoize on
  (remaining, last_was_one): only 2(n+1) states.
- **Variant seeds:** count tilings of a 1×n strip with 1- and 2-wide tiles written as two calls;
  count strings over {a, b} with no "aa" where the branch is guarded by the previous letter.
- **Verified:** derivation ×2 + empirical op-count
- **Retired:** —

## RR-08
- **Trick:** sqrt-shrink-recurrence
- **Difficulty:** 3/3
- **Time:** Θ(log log u)
- **Space:** Θ(log log u)
- **Why:** T(u) = T(√u) + O(1). Substitute m = log₂ u: S(m) = S(m/2) + 1 → Θ(log m) = Θ(log log u).
  Re-derivation: after k calls the value is u^{1/2^k}; it reaches ≤ 2 when 2^k ≥ log₂ u, i.e.
  k = log₂ log₂ u. Every call is a frame on the stack, so space is the same Θ(log log u).
- **Common wrong answers:** Θ(log u) (treats taking √ like halving); Θ(√u) (confuses the value with
  the work); Θ(1) space ("it's tiny" — it is tiny, but it grows).
- **Probe questions:** "u = 2⁶⁴: roughly how many calls?" → exponent goes 64 → 32 → 16 → 8 → 4 → 2 → 1,
  about 6–7 calls. "What if it called `rr08(cluster_size)` twice?" → T(u) = 2T(√u) + 1 → S(m) = 2S(m/2)
  + 1 → Θ(m) = Θ(log u).
- **Variant seeds:** T(u) = T(√u) + log u disguised as a per-level loop over the bits → S(m) = S(m/2) +
  m → Θ(log u); `n = int(n ** 0.5)` inside a recursive "vEB height" helper with a list-length input.
- **Verified:** derivation ×2 + empirical op-count (via substitution u = 2^m, fit Θ(log m))
- **Retired:** —

## RR-09
- **Trick:** linear-peel-recurrence
- **Difficulty:** 1/3
- **Time:** Θ(n²)
- **Space:** Θ(n)
- **Why:** T(k) = T(k − 1) + Θ(k) (scan the first k, then recurse on k − 1) → n(n−1)/2 comparisons →
  Θ(n²). Space: the recursive call is last, but CPython keeps every frame → n frames → Θ(n).
- **Common wrong answers:** Θ(n) time (sees a single recursive call and forgets the per-call loop);
  Θ(1) space ("it sorts in place" — the data is in place, the stack isn't); Θ(n log n) time.
- **Probe questions:** "Best case on already-sorted input?" → still Θ(n²): the scan never exits early.
  "Get Θ(1) space?" → turn it into a `for k in range(n, 1, -1)` loop.
- **Variant seeds:** recursive "remove the minimum, recurse on the rest" via a start index; recursive
  insertion sort `insert_last(k)` (T(k−1) + k worst case).
- **Verified:** derivation ×2 + empirical op-count
- **Retired:** —

## RR-10
- **Trick:** permutations-enumeration
- **Difficulty:** 2/3
- **Time:** Θ(n·n!)
- **Space:** Θ(n·n!) (the returned list is counted, as the problem states)
- **Why:** The tree has n·(n−1)·…·(n−k+1) = n!/(n−k)! nodes at depth k; all internal levels together
  have ≈ (e − 1)·n! nodes, so the loop/swap overhead is Θ(n!). The n! leaves each `snapshot` in Θ(n) →
  Θ(n·n!) dominates. Space: n! stored lists of length n → Θ(n·n!); stack depth n + 1 is negligible.
- **Common wrong answers:** Θ(n!) time (forgets the O(n) copy per leaf); Θ(nⁿ) (thinks every level has n
  choices); Θ(n) space (forgets that this problem counts the output); Θ(n!) space (counts lists, not
  elements).
- **Probe questions:** "Auxiliary space excluding the output?" → Θ(n): stack depth n, swaps are in
  place. "Why not nⁿ?" → each level has one fewer choice: n·(n−1)·…·1.
- **Variant seeds:** permutations with a `used[]` array that print each arrangement in O(n), output not
  counted (Θ(n·n!) time, Θ(n) space); k-permutations of n (Θ(k·n!/(n−k)!) leaves cost).
- **Verified:** derivation ×2 + empirical op-count
- **Retired:** —

## RR-11
- **Trick:** stack-depth-vs-total-calls
- **Difficulty:** 3/3
- **Time:** Θ(n²)
- **Space:** Θ(log n)
- **Best:** Θ(n log n)
- **Why:** Worst time: an adversary places p at an end each time; the empty side returns instantly and
  the loop continues on n − 1, n − 2, … → Θ(n²) partition work. Space: the function recurses only on
  the *smaller* side (size ≤ half) and handles the larger side by looping in the same frame, so each
  new frame at least halves the segment → depth ≤ log₂ n + 1 → Θ(log n) even in the worst case.
  Best time: balanced pivots → T(n) = 2T(n/2) + n → Θ(n log n).
- **Common wrong answers:** Θ(n) space (classic quicksort worst-case depth — misses the smaller-side
  trick); Θ(1) space (sees the `while` loop, misses the recursive calls); Θ(n log n) worst time
  (assumes good pivots); Best Θ(n) (every element is touched once per level, and there are ≥ log n
  levels).
- **Probe questions:** "Which pivot pattern makes the stack deepest?" → balanced (median) pivots —
  the fastest case gives the deepest stack; end pivots give depth O(1). "What if it always recursed on
  the left part and looped on the right?" → worst-case depth Θ(n) (p = hi every time).
- **Variant seeds:** quickselect that recurses on the side containing k and loops otherwise (depth vs
  time divergence); DFS on a tree where the code recurses on the lighter child and iterates down the
  heavier one (Θ(log n) stack, Θ(n) time).
- **Verified:** derivation ×2 + empirical op-count (incl. brute-force max depth over all pivot
  sequences)
- **Retired:** —

## RR-12
- **Trick:** balanced-split-constant-work
- **Difficulty:** 2/3
- **Time:** Θ(n)
- **Space:** Θ(log n)
- **Why:** T(n) = 2T(n/2) + O(1) → Θ(n): the call tree is a full binary tree with n leaves, so 2n − 1
  calls. Master case 1 agrees: n^{log₂ 2} = n beats f(n) = 1. Space: depth ⌈log₂ n⌉ + 1 → Θ(log n).
- **Common wrong answers:** Θ(log n) time (sees halving, like binary search — but both halves are
  visited); Θ(n log n) (assumes Θ(n) work per level *per call*); Θ(n) space (counts total calls instead
  of the live path).
- **Probe questions:** "Exactly how many calls for n = 8?" → 15. "If each call also looped over
  lo..hi?" → 2T(n/2) + n → Θ(n log n).
- **Variant seeds:** recursive count of zeros in a range by halves; recursive segment-tree build that
  stores one value per node (time Θ(n), space Θ(n) for the tree).
- **Verified:** derivation ×2 + empirical op-count
- **Retired:** —

## RR-13
- **Trick:** three-way-branching
- **Difficulty:** 1/3
- **Time:** Θ(3ⁿ)
- **Space:** Θ(n)
- **Why:** T(n) = 3T(n − 1) + O(1) → 3ⁿ leaves, (3^{n+1} − 1)/2 calls; each leaf does `max` over 3
  loads, O(1). Space: `loads` is O(1), and the stack holds one path of n + 1 frames → Θ(n).
- **Common wrong answers:** Θ(n³) (confuses 3 branches with 3 nested loops); Θ(2ⁿ) (pattern-matches
  "subset recursion"); Θ(3ⁿ) space (counts total calls); Θ(n·3ⁿ) time (thinks the leaf check is O(n)).
- **Probe questions:** "With s servers?" → Θ(sⁿ) leaves and each leaf does max over s loads → Θ(s·sⁿ)
  time, Θ(n + s) space. "Easy pruning to cut work?" → assign job 0 to server 0 only (symmetry) — still
  Θ(3ⁿ) asymptotically.
- **Variant seeds:** color n houses with R/G/B by recursion; enumerate all length-n strings over
  {'L', 'R', 'S'} and evaluate each in O(1) with running state.
- **Verified:** derivation ×2 + empirical op-count
- **Retired:** —

## RR-14
- **Trick:** two-dimensional-memo
- **Difficulty:** 3/3
- **Time:** Θ(k·n²)
- **Space:** Θ(k·n)
- **Why:** State = (i, pieces), pieces ∈ 2..k, i over ~n − k + 1 reachable values → Θ(k·n) states, each
  computed once. Each state loops over up to n − pieces + 1 − i positions; with k ≤ n/2 a constant
  fraction of states loop Θ(n) times → Θ(k·n²) (precisely ≈ (k−1)(n−k)²/2 iterations). Each inner
  call is O(1) on a hit; misses are charged to their own state. Space: memo Θ(k·n) + suffix Θ(n) +
  stack depth k → Θ(k·n).
- **Common wrong answers:** Θ(k·n) time (counts states but forgets the loop inside each state);
  Θ(n²) (drops k); Θ(n^k) or C(n, k) (ignores the memo); Θ(k) or Θ(n) space (counts only the stack or
  only `suffix`).
- **Probe questions:** "Why does the constraint k ≤ n/2 matter?" → reachable states shrink as k → n;
  the exact count is Θ(k·(n−k)²), which equals Θ(k·n²) only when n − k = Θ(n). "A faster approach?" →
  binary search on the answer with a greedy check: O(n log(sum(nums))).
- **Variant seeds:** palindrome-partition min cuts with memo(i, j) and an inner loop → Θ(n³) time,
  Θ(n²) space; edit distance memo(i, j) with O(1) per state → Θ(m·n) time and space, depth Θ(m + n).
- **Verified:** derivation ×2 + empirical op-count
- **Retired:** —

## RR-15
- **Trick:** merge-sort-recurrence
- **Difficulty:** 2/3
- **Time:** Θ(n log n)
- **Space:** Θ(n)
- **Why:** T(n) = 2T(n/2) + Θ(n) → Θ(n log n). Space: `merged` (size hi − lo) is created only after both
  recursive calls have returned and is freed when the call returns, so at most one buffer is alive at a
  time; the largest is n at the root → Θ(n), plus Θ(log n) stack.
- **Common wrong answers:** Θ(log n) space (counts only the stack, misses the merge buffer); Θ(n log n)
  space (adds up every call's buffer as if all were alive at once — that is total *allocation*, not peak
  memory); Θ(n²) time.
- **Probe questions:** "If `merged` were allocated before the recursive calls and filled after?" →
  buffers along one root-to-leaf path are alive: n + n/2 + … → still Θ(n). "Total memory allocated over
  the whole run?" → Θ(n log n), but never simultaneously.
- **Variant seeds:** inversion count that merges into one preallocated temp array passed down
  (Θ(n) space, same time); bottom-up iterative merge sort with width doubling (Θ(n log n), Θ(n), no
  stack).
- **Verified:** derivation ×2 + empirical op-count
- **Retired:** —
