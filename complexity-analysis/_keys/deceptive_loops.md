# Keys — deceptive_loops.py (tutor only — learner does not open)

## DL-01
- **Trick:** early-break-worst-case
- **Difficulty:** 2/3
- **Time:** Θ(n²)
- **Space:** Θ(1)
- **Best:** Θ(n)
- **Why:** Worst case (no pair sums to `target`): `break` never fires, so the inner loop runs
  n−1−i times for each i → Σ = n(n−1)/2 = Θ(n²). Best case (e.g. all zeros, target 0): every inner
  loop breaks at j = i+1, but `break` only leaves the *inner* loop, so the outer loop still runs n
  times → Θ(n).
- **Common wrong answers:** Θ(n) worst (thinks `break` makes the scan stop early in general — worst
  case is the input where it never fires); Θ(1) best (thinks `break` exits both loops — it only
  exits the innermost); Θ(n log n) (vague "break saves about half").
- **Probe questions:** "Which input makes this slowest?" → any input with no pair summing to
  target, e.g. all distinct values and an impossible target. "Change `break` to `return hits` —
  best case now?" → Θ(1); worst case is still Θ(n²).
- **Variant seeds:** search a 2D grid row by row with `break` on the first match in each row
  (worst Θ(n·m), best Θ(n)); a `for…else` loop where the `else` triggers an expensive rescan.
- **Verified:** derivation ×2 + empirical op-count
- **Retired:** —

## DL-02
- **Trick:** log-factorial-sum
- **Difficulty:** 3/3
- **Time:** Θ(n log n)
- **Space:** Θ(1)
- **Why:** The inner loop walks from `node` up to the root: ⌊log₂ node⌋ steps. Total =
  Σ_{v=1..n} ⌊log₂ v⌋ ≈ log₂(n!) = Θ(n log n). Lower bound: the n/2 nodes in [n/2, n] each take
  ≥ log₂ n − 1 steps. Most nodes of a complete tree live near the bottom, so they are *deep*.
- **Common wrong answers:** Θ(n) (confuses this with "heapify is O(n)" — heapify sums node
  *heights*, which are small for most nodes; this sums *depths*, which are large for most nodes);
  Θ(log n) (only looks at one walk); Θ(n²) (sees nested loops).
- **Probe questions:** "Why is building a heap O(n) but this is O(n log n)?" → heapify's cost per
  node is its height (distance *down* to the leaves), and most nodes are near the leaves, so
  heights are small; here the cost is depth (distance *up* to the root), and most nodes are deep.
  "Give a lower bound without Stirling" → the last n/2 nodes each cost ≥ log₂(n/2).
- **Variant seeds:** count the bits of every integer 1..n with `while x: x >>= 1`; for each i,
  run a binary search over `nums[:i]`'s index range (lo=0, hi=i) without slicing.
- **Verified:** derivation ×2 + empirical op-count
- **Retired:** —

## DL-03
- **Trick:** different-size-loops
- **Difficulty:** 1/3
- **Time:** Θ(n·m)
- **Space:** Θ(n) — this is the returned `assignment` list. If the learner explicitly excludes the
  output from auxiliary space, Θ(1) is a Pass.
- **Why:** 10 (a constant) rounds × n points × (m−1) centers × O(1) `dist` = Θ(n·m). The round
  loop is constant and drops out. `assignment` is a fresh list of n ints → Θ(n) auxiliary.
- **Common wrong answers:** Θ(n²) (treats both loops as size n — they are different inputs);
  Θ(n·m·10) written as a distinct class (fine in substance but constants drop: say Θ(n·m));
  Θ(n³) (counts the round loop as another n); Space Θ(1) (forgets `assignment`) or Θ(m).
- **Probe questions:** "If the number of rounds were `r` (an input), what then?" → Θ(r·n·m).
  "When could you write this as O(n)?" → only if m is bounded by a constant (e.g. always 3
  centers).
- **Variant seeds:** for each word in `words`, scan every character of `pattern` (Θ(n·p));
  for each row in an n×m grid, for each column, for each of 4 neighbors (Θ(n·m), the 4 drops).
- **Verified:** derivation ×2 + empirical op-count (m = n, m fixed, n fixed)
- **Retired:** —

## DL-04
- **Trick:** geometric-inner-loop
- **Difficulty:** 3/3
- **Time:** Θ(n)
- **Space:** Θ(log n)
- **Why:** Stride takes values 1, 2, 4, …, < n, and the inner loop runs ⌈n/stride⌉ times:
  n + n/2 + n/4 + … ≤ 2n (+ log n for the ceilings) = Θ(n). `peaks` gets one entry per stride
  value → ⌈log₂ n⌉ entries → Θ(log n) auxiliary space.
- **Common wrong answers:** Θ(n log n) (multiplies log n outer passes × n, but each pass is half
  the previous); Θ(n²) (sees nested loops); Space Θ(1) (misses that `peaks` grows with the number
  of passes) or Θ(n) (assumes `peaks` grows per element).
- **Probe questions:** "What if `stride += 1` instead of `stride *= 2`?" → harmonic sum n/1 + n/2
  + … + n/n = Θ(n log n). "What if the inner loop were `range(stride)` instead?" → 1 + 2 + 4 + …
  < 2n, still Θ(n).
- **Variant seeds:** `stride *= 3` with inner `range(0, n, stride)`; outer `size = n; while size:
  … size //= 2` with inner `range(size)`.
- **Verified:** derivation ×2 + empirical op-count (time and len(peaks))
- **Retired:** —

## DL-05
- **Trick:** triangular-nested-loop
- **Difficulty:** 1/3
- **Time:** Θ(n²)
- **Space:** Θ(n)
- **Why:** The list shrinks by one per round (`pop()` removes just the last item, O(1)), so the
  inner scan does n, n−1, …, 1 steps: n(n+1)/2 = Θ(n²). `list(tasks)` copies the input → Θ(n).
- **Common wrong answers:** Θ(n log n) or Θ(n) (feels like "the work keeps shrinking", but it
  shrinks by 1, not by half); Θ(n²/2) as a different class (constants drop); Space Θ(1) (forgets
  the copy).
- **Probe questions:** "What change would make this Θ(n)?" → remove half the list each round
  (e.g. `del pending[len(pending)//2:]`), giving n + n/2 + … < 2n. "Is `pop()` the bottleneck?"
  → no, `pop()` from the end is O(1); `pop(0)` would add Θ(n) per round but the total stays Θ(n²).
- **Variant seeds:** `for i in range(n): for j in range(i): …` hidden as "compare each new item
  with all earlier ones"; a `while lo < hi` loop that scans `range(lo, hi)` then does `lo += 1`.
- **Verified:** derivation ×2 + empirical op-count
- **Retired:** —

## DL-06
- **Trick:** sliding-window-amortized
- **Difficulty:** 2/3
- **Time:** Θ(n)
- **Space:** Θ(min(n, k))
- **Why:** `right` advances n times. `left` only ever increases and never passes `right`, so the
  inner `while` runs at most n times *in total* across the whole function → Θ(n + n) = Θ(n)
  (dict ops are O(1) average). The dict holds at most k+1 keys and at most n keys →
  Θ(min(n, k)) (also bounded by alphabet size; O(k) is a Pass).
- **Common wrong answers:** Θ(n²) (charges the inner `while` up to n per outer iteration instead
  of n total); Θ(n·k) (thinks each shrink costs k); Space Θ(1) (forgets the dict grows with k —
  only valid if the learner explicitly assumes a fixed alphabet, then probe) or Θ(n) (loose when
  k ≪ n; Partial).
- **Probe questions:** "How many times can `left += 1` execute over the whole run?" → at most n,
  because `left` never decreases and never exceeds `right`. "If you replaced the `while` with
  recomputing distinct counts of `s[left:right+1]` each step, what then?" → Θ(n²) or worse.
- **Variant seeds:** longest subarray with sum ≤ budget on non-negative ints (Θ(n), Θ(1));
  minimum-window covering all characters of `t` (Θ(n + m)).
- **Verified:** derivation ×2 + empirical op-count (time for k = 2, 5, n/2; dict size for k = n/4)
- **Retired:** —

## DL-07
- **Trick:** repeated-squaring-loop
- **Difficulty:** 3/3
- **Time:** Θ(log log n)
- **Space:** Θ(1)
- **Why:** After t passes `width = 2^t`, and the loop continues while 2^width < n, i.e. while
  width < log₂ n. So it stops once 2^t ≥ log₂ n → t = ⌈log₂ log₂ n⌉. Doubling the *exponent*
  squares the value `1 << width`, which is the `i = i*i` pattern in disguise.
- **Common wrong answers:** Θ(log n) (sees `width *= 2` and pattern-matches "doubling → log n" —
  but it is the exponent doubling, not the compared value); Θ(1) (thinks it is just a handful of
  steps — true in practice, but it grows unboundedly); Θ(n).
- **Probe questions:** "What does `1 << width` do each pass?" → it squares: 2^(2w) = (2^w)².
  "If the line were `width += 1`, what then?" → Θ(log n).
- **Variant seeds:** `x = 2; while x < n: x = x * x`; `while n > 2: n = int(n ** 0.5)`
  (shrinks by square root each step).
- **Verified:** derivation ×2 + empirical op-count (n = 2^(2^k) + 1 up to k = 13)
- **Retired:** —

## DL-08
- **Trick:** harmonic-sum
- **Difficulty:** 2/3
- **Time:** Θ(n log n)
- **Space:** Θ(n)
- **Why:** For each d the inner loop visits the multiples d, 2d, …, ≤ n: ⌊n/d⌋ steps. Total =
  n(1 + 1/2 + 1/3 + … + 1/n) = n·H_n = Θ(n log n). `divisor_count` is n+1 ints → Θ(n).
- **Common wrong answers:** Θ(n²) (sees nested loops up to n); Θ(n) (thinks the step size makes
  inner loops "basically constant"); Θ(n log log n) (confuses with the prime sieve, which only
  sieves from primes); Θ(n√n) (confuses with trial division, cf. DL-10).
- **Probe questions:** "Why isn't this the Sieve of Eratosthenes bound?" → the prime sieve only
  runs the inner loop for prime d (Σ_{p ≤ n} n/p = Θ(n log log n)); here every d runs.
  "What is 1 + 1/2 + … + 1/n?" → ≈ ln n.
- **Variant seeds:** for each gap g in 1..n, compare `nums[i]` with `nums[i+g]` for i stepping by
  g; mark every multiple of every element of a set of n distinct values ≤ n.
- **Verified:** derivation ×2 + empirical op-count
- **Retired:** —

## DL-09
- **Trick:** triple-nested-combinations
- **Difficulty:** 2/3
- **Time:** Θ(n³)
- **Space:** Θ(n)
- **Why:** `combinations(nums, 3)` yields every i < j < k triple: C(n, 3) = n(n−1)(n−2)/6 =
  Θ(n³), each O(1). One visible loop, three hidden ones. Space: the generator yields one tuple at a
  time, but CPython's `combinations` first copies its input into a tuple (`tuple(nums)`), so a list
  input costs Θ(n) auxiliary (it would be Θ(1) only if `nums` were already a tuple).
- **Common wrong answers:** Θ(n) (counts the single `for` — the loop runs C(n,3) times, not n);
  Θ(n²) (thinks "choose" sizes are small); "n³/6 is less than n³" (constants drop); Space Θ(1)
  (assumes the generator is fully lazy — its output is lazy, its input pool is not). Grade Θ(1)
  with lazy-generator reasoning as a **Pass** — this is CPython trivia, not the trick under test —
  then share the pool-copy fact as an FYI); Space Θ(n³) (thinks all triples are materialized).
- **Probe questions:** "How many times does the loop body run for n = 10?" → C(10,3) = 120.
  "What about `combinations(nums, 2)` and `permutations(nums, 3)`?" → Θ(n²) and Θ(n³)
  (n(n−1)(n−2), 6× more but same class).
- **Variant seeds:** explicit `for i … for j in range(i+1, n) … for k in range(j+1, n)` hidden as
  "count valid triangles"; a double loop over pairs with an inner `while k < n` scan that never
  breaks.
- **Verified:** derivation ×2 + empirical op-count (time; pool copy confirmed with tracemalloc)
- **Retired:** —

## DL-10
- **Trick:** divisor-iteration
- **Difficulty:** 3/3
- **Time:** Θ(n√n)
- **Space:** Θ(1)
- **Why:** Trial division of x tries d = 1..⌊√x⌋ (the `x % d` test runs every time, divisor or
  not), so x costs Θ(√x). Total = Σ_{x=1..n} √x ≈ (2/3)·n^{3/2}. Lower bound: the n/2 values in
  [n/2, n] each cost ≥ √(n/2) → Ω(n^{3/2}).
- **Common wrong answers:** Θ(√n) (analyzes one x); Θ(n log n) (assumes the work is only done for
  actual divisors, ~log n on average — but the loop header runs √x times regardless of the `if`);
  Θ(n²) (thinks trial division goes up to x).
- **Probe questions:** "Does the `if x % d == 0` reduce how many times the loop runs?" → no, it
  only gates the body; the `while` runs ⌊√x⌋ times regardless. "How does DL-08 do the same job
  faster?" → it flips the loops (for each d, visit its multiples) → Θ(n log n).
- **Variant seeds:** for each x in 1..n, try every d in 1..x and count divisors (Θ(n²)); check
  primality of every element of an array of n values each ≤ V by trial division (Θ(n√V)).
- **Verified:** derivation ×2 + empirical op-count
- **Retired:** —

## DL-11
- **Trick:** two-pointer-nested-while
- **Difficulty:** 1/3
- **Time:** Θ(n)
- **Space:** Θ(1)
- **Why:** The inner loop only advances j, and the outer loop resumes from `i = j`, so every index
  is visited by the inner loop exactly once in total → Θ(n). The outer loop runs once per run of
  equal characters (≤ n).
- **Common wrong answers:** Θ(n²) (charges the inner loop up to n per outer iteration — it can be
  long only when the outer loop then skips that much).
- **Probe questions:** "What if the last line were `i += 1` instead of `i = j`?" → Θ(n²) for a
  string of one repeated character (each i rescans its run to the end). "How many outer iterations
  for 'aaabbc'?" → 3.
- **Variant seeds:** remove duplicates from a sorted array with an inner `while nums[j] == nums[i]`
  skip; merge overlapping intervals where an inner `while` absorbs every interval that overlaps.
- **Verified:** derivation ×2 + empirical op-count (random, one run, all distinct)
- **Retired:** —

## DL-12
- **Trick:** geometric-inner-loop
- **Difficulty:** 2/3
- **Time:** Θ(n)
- **Space:** Θ(n)
- **Why:** Each round halves the list: n + n/2 + n/4 + … ≤ 2n (plus ≤ log n for rounding up) →
  Θ(n), even though there are log n rounds. `level` is a copy of size n and `nxt` is up to n/2 →
  Θ(n) auxiliary.
- **Common wrong answers:** Θ(n log n) (log n rounds × "n per round" — but the rounds shrink);
  Θ(log n) (counts only rounds); Space Θ(log n) (thinks only round count matters) or Θ(1)
  (forgets the copy).
- **Probe questions:** "If each round also re-scanned the original full `values` list, what
  then?" → Θ(n log n). "What's the peak memory?" → about n + n/2 references at once, still Θ(n).
- **Variant seeds:** bottom-up merge passes where each pass only touches surviving "winners";
  repeatedly keep the larger half of a list until one element remains.
- **Verified:** derivation ×2 + empirical op-count (powers of two and 2^k + 1 sizes)
- **Retired:** —

## DL-13
- **Trick:** harmonic-sum
- **Difficulty:** 3/3
- **Time:** Θ(n log n)
- **Space:** Θ(1)
- **Why:** For a given `size`, the inner loop runs over starts 0, size, 2·size, … ≤ n−size: ⌊n/size⌋
  steps, each O(1) thanks to prefix sums. Total = Σ_{s=1..n} ⌊n/s⌋ ≈ n·ln n = Θ(n log n).
- **Common wrong answers:** Θ(n²) (sees `for size in range(1, n+1)` with an inner loop and assumes
  the inner loop is ~n each time — it is n/size); Θ(n) (confuses with doubling sizes, cf. DL-04);
  Θ(n³) (thinks each chunk sum is computed by scanning the chunk — prefix sums make it O(1)).
- **Probe questions:** "If `size *= 2` instead of `size += 1`, what then?" → geometric: Θ(n).
  "If the chunk sum were `sum(values[start:start+size])` instead of a prefix difference?" →
  each size costs Θ(n) total → Θ(n²).
- **Variant seeds:** for every period p in 1..n, compare `s[i]` to `s[i+p]` only at indices that
  are multiples of p; for each k in 1..n, do O(1) work on every k-th element.
- **Verified:** derivation ×2 + empirical op-count
- **Retired:** —

## DL-14
- **Trick:** sqrt-bound-loop
- **Difficulty:** 2/3
- **Time:** Θ(√n)
- **Space:** Θ(1)
- **Why:** After r iterations `used` = 1 + 2 + … + r = r(r+1)/2. The loop stops once that would
  exceed n, so r(r+1)/2 ≤ n → r ≈ √(2n) = Θ(√n). The stopping value grows quadratically in the
  counter, which is `i*i < n` in disguise.
- **Common wrong answers:** Θ(n) (thinks each coin is placed one step at a time — each step places
  a whole row of `rows` coins); Θ(log n) (assumes "growing step size" means doubling); Θ(1).
- **Probe questions:** "What's `used` after r rows?" → r(r+1)/2. "If `rows` doubled each step
  (rows *= 2; used += rows), what then?" → Θ(log n).
- **Variant seeds:** `i = 1; while i * i <= n: i += 1` disguised as an integer-sqrt search;
  `step = 0; pos = 0; while pos < n: step += 1; pos += 2 * step - 1` (pos = step²).
- **Verified:** derivation ×2 + empirical op-count
- **Retired:** —

## DL-15
- **Trick:** halving-while-in-for
- **Difficulty:** 1/3
- **Time:** Θ(n log n)
- **Space:** Θ(1)
- **Why:** For each of the n elements, a fresh binary search over the full range [0, n) halves
  `hi − lo` each step → ⌈log₂(n+1)⌉ steps. The range resets every outer iteration, so the costs
  multiply: n × Θ(log n) = Θ(n log n).
- **Common wrong answers:** Θ(log n) (analyzes one search); Θ(n) (thinks halving loops are "cheap"
  or amortize — they would only if `lo`/`hi` persisted across iterations); Θ(n²) (sees nested loops).
- **Probe questions:** "What if `lo, hi = 0, n` were moved above the `for` (not reset)?" → after
  the first search the range is empty, so total Θ(n + log n) = Θ(n) (and the result is wrong).
  "What if each search ran over [0, i) instead of [0, n)?" → Σ log i = Θ(n log n) still.
- **Variant seeds:** `for i in range(n): j = n; while j > 0: j //= 2`; for each of m queries,
  binary-search a sorted array of length n (Θ(m log n)).
- **Verified:** derivation ×2 + empirical op-count
- **Retired:** —
