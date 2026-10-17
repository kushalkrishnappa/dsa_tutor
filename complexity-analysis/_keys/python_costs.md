# Keys — python_costs.py (tutor only — learner does not open)

Convention for this file: hash-table operations (`in`/get/set on dict and set) are graded at their
interview-standard **expected O(1)** for O(1)-sized keys. Adversarial-collision O(n) worst case is a
good aside but not the expected answer. Unless a key says otherwise, the returned value counts toward
SPACE if the function builds it. If the learner explicitly leaves out the output and says so, accept the
smaller bound.

## PY-01
- **Trick:** hash-key-cost
- **Difficulty:** 2/3
- **Time:** Θ((n−k+1)·k), which is O(n·k). That's Θ(n²) when k ≈ n/2 and Θ(n) when k is a constant.
- **Space:** Θ((n−k+1)·k), which is O(n·k). Worst case every window is distinct and stored.
- **Why:** There are n−k+1 iterations. Each one does `s[i:i+k]`, which copies k chars (O(k)). It then
  hashes that new string for `in` and `add`, which reads all k chars (O(k)). A string caches its hash
  only after the first computation, and every slice is a new object, so nothing is reused. A hash hit
  also runs an O(k) equality check. So each window costs Θ(k).
- **Common wrong answers:** O(n) time (treats set ops as O(1) whatever the key length, and forgets the
  slice). O(n) space (counts the entries, not the k chars inside each one). O(n²) (right only when
  k = Θ(n); a Miss if the learner drops k completely).
- **Probe questions:** "LeetCode 187 (Repeated DNA Sequences) fixes k = 10. What's the cost then?" →
  Θ(n), since k is a constant. "How would you get O(n) for any k?" → a rolling hash (Rabin–Karp) that
  stores integers, which brings the per-window cost down to O(1) expected.
- **Variant seeds:** memoize a recursion with key `tuple(remaining_list)` or `str(path)`. Count the
  distinct rows of an r×c grid with `set(tuple(row) for row in grid)`. That's Θ(r·c), not Θ(r).
- **Verified:** derivation ×2 + empirical timing (k=n/4 fits n², fixed n vs k fits (n−k+1)·k,
  k=10 fits n) + tracemalloc peak (fits n² at k=n/4)
- **Retired:** —

## PY-02
- **Trick:** list-index
- **Difficulty:** 1/3
- **Time:** Θ(n²)
- **Space:** Θ(n)
- **Why:** `sorted` costs Θ(n log n) once. Then `order.index(x)` runs a linear scan that stops at x's
  position. For distinct values the positions are 0…n−1, so the total is Σ i ≈ n²/2. The scans
  dominate. Space: the `order` copy plus `ranks`.
- **Common wrong answers:** Θ(n log n) (counts the sort and treats `.index` as O(1), like a dict
  lookup). Θ(n) space is right; Θ(1) space misses the sorted copy.
- **Probe questions:** "Make it Θ(n log n)." → build `{v: i for i, v in enumerate(order)}` once, then
  each rank is an O(1) lookup. "Best case?" → all values equal: every `.index` returns 0 in O(1) and Timsort
  is Θ(n) on equal input, so Θ(n) overall.
- **Variant seeds:** `sorted(set(s), key=s.index)` (first-occurrence order, Θ(n·d)). Two-sum that
  calls `nums.index(target - x)` inside the loop.
- **Verified:** derivation ×2 + empirical timing + tracemalloc peak
- **Retired:** —

## PY-03
- **Trick:** path-copy-recursion
- **Difficulty:** 3/3
- **Time:** Θ(n²) worst case (skewed tree). More precisely O(n·h), and Θ(n log n) for a balanced tree.
- **Space:** Θ(n²) worst case (skewed). More precisely Θ(h²).
- **Why:** `path + [node.val]` builds a new list of length depth+1 at every node. Total copying is
  Σ depth = O(n·h), and a chain makes it n²/2. Leaf checks cost O(depth) each and don't change the
  bound. Space: each frame on the current stack keeps its own path copy alive, so lengths 1, 2, …, h are
  alive at once, giving Θ(h²), plus a Θ(h) stack.
- **Common wrong answers:** Θ(n) time ("visit each node once" — misses the copy at each node). Θ(h)
  or Θ(n) space (counts only the stack, or only one path). Θ(n log n) as the worst case (assumes the
  tree is balanced).
- **Grading note:** O(n·h) time with O(h²) space, worst case n², is a full Pass. Θ(n log n) with no
  mention of the skewed case is a Miss on worst case. If they write Θ(n log n) and clearly limit it
  to balanced trees, give Partial and probe with the skewed case.
- **Probe questions:** "Rewrite it with `path.append(...)` / `path.pop()` and one shared list. What's
  the cost now?" → Θ(n) time apart from the O(depth) palindrome check at leaves. Space becomes Θ(h),
  but time stays O(n·h) worst case because of the leaf checks. "Where do the h² copies live?" → one
  per suspended stack frame.
- **Variant seeds:** subset or combination backtracking that passes `cur + [x]` (with the output
  excluded). DFS on a grid path that passes `visited | {cell}` (set copy).
- **Verified:** derivation ×2 + empirical timing (skewed: n²) + tracemalloc peak (skewed: n²) +
  op-count of copied elements (complete tree: n log n)
- **Retired:** —

## PY-04
- **Trick:** str-concat
- **Difficulty:** 2/3
- **Time:** Θ(n²) worst case by the language's guarantee. CPython usually runs this exact code in
  Θ(n) (see the note).
- **Space:** Θ(n)
- **Why:** `str` is immutable, so in principle `cleaned += c` builds a new string and copies everything
  so far: 1 + 2 + … + n = Θ(n²). CPython has an implementation-specific shortcut. When the left side is
  a plain local variable (or a global), the result is stored right back into it, and the string has no
  other reference (refcount 1), the interpreter resizes the string in place with `realloc`. In 3.11+
  this is the specialized opcode `BINARY_OP_INPLACE_ADD_UNICODE`. That makes each append amortized
  O(1) in practice. The language doesn't promise this. PyPy behaves differently, and any second
  reference turns it off (an alias, an attribute such as `self.s`, a list slot, or a prepend
  `c + s`).
- **Measured on this machine (CPython 3.14.7, macOS arm64):** the code as written grows linearly
  (2^14–2^21 chars). Adding one alias (`alias = cleaned` in the loop) or using an attribute
  accumulator makes it quadratic. `out = out + ch` is also optimized (linear). `out = ch + out` is
  quadratic. `"".join(parts)` is linear.
- **How to grade TIME:**
  - Pass: Θ(n²), because strings are immutable and each `+=` may copy the prefix. Mentioning
    `"".join` earns a bonus but isn't required.
  - Pass: Θ(n), but only if the learner names the CPython refcount-1 in-place resize and says it is
    not guaranteed (that the portable worst case is n²).
  - Partial: Θ(n) citing CPython's optimization without saying it's implementation-specific. Probe:
    "Would this still hold on PyPy, or if another variable pointed at `cleaned`?"
  - Miss: Θ(n) reasoned as "`+=` is O(1) like list append" (thinks strings are mutable).
- **Common wrong answers:** Θ(n) "because appending is O(1)" (confuses str with list). Θ(n²) space
  (adds up all the temporary copies, but each old copy is freed, so at most two are alive).
- **Probe questions:** "What's the guaranteed-linear idiom?" → collect the chars in a list and
  `"".join` once, which is Θ(total length). "Name one change that kills the CPython optimization." →
  keep a second reference, accumulate into `self.x` or `d[k]`, or prepend.
- **Variant seeds:** build a reversed string with `rev = ch + rev` (always Θ(n²)). Build CSV output
  with `self.buf += row` inside a method.
- **Verified:** derivation ×2 + empirical timing (as written: n; with an alias or attribute: about n²)
  + tracemalloc peak (n) + `dis` shows `BINARY_OP_INPLACE_ADD_UNICODE`
- **Retired:** —

## PY-05
- **Trick:** constant-time-builtins
- **Difficulty:** 2/3
- **Time:** Θ(n)
- **Space:** Θ(k)
- **Why:** This is a reverse trap. `first.keys()` returns a view, not a list (a list was Python 2
  behavior). `x in view` is a hash lookup, O(1) expected. `len(dict)` and `len(list)` read a stored
  size field in O(1). The loop runs at most n times, and in the worst case there are fewer than k
  distinct values, so it scans everything. The final `list(first.keys())` runs once and costs
  Θ(len) ≤ k. The dict and the result each hold ≤ k entries.
- **Common wrong answers:** Θ(n²) or Θ(n·k) (thinks `.keys()` builds a list each time, or that `len`
  counts elements). Θ(n) space (also fine as a loose bound, so Partial: the dict is capped at k).
- **Probe questions:** "What if it were `x not in list(first.keys())`?" → that builds an O(k) list
  every iteration, so Θ(n·k). "Is `len(s)` on a string O(1)?" → yes, the length is stored.
- **Variant seeds:** `while len(stack) > 0:` in a monotonic-stack loop (still Θ(n)). `if key in
  counts.keys()` inside a frequency-count loop, compared with `if key in list(counts)`.
- **Verified:** derivation ×2 + empirical timing (in-cache sizes, plus a k > #distinct full scan:
  both n) + tracemalloc peak. At sizes beyond the cache, dict access drifts slightly above linear
  because of cache misses, not because of the asymptotics.
- **Retired:** —

## PY-06
- **Trick:** slice-copy
- **Difficulty:** 1/3
- **Time:** Θ(n²)
- **Space:** Θ(n)
- **Why:** `rest[1:]` copies the remaining n−1, n−2, … pointers. Total: Σ = n(n−1)/2. Only about one
  or two slices are alive at once (the old one is freed when `rest` is rebound), so peak extra memory
  is Θ(n).
- **Common wrong answers:** Θ(n) time (treats a slice as an O(1) view, the way NumPy or Go do). Θ(n²)
  space (adds up every slice ever made, but each is freed right away).
- **Probe questions:** "Fix it without changing the loop shape." → walk an index `i` instead of
  slicing, or use `itertools.islice` / `memoryview` (for bytes). "Is `nums[::-1]` cheaper?" → no,
  it's also an O(n) copy.
- **Variant seeds:** `while queue: x, queue = queue[0], queue[1:]`. A binary search that recurses on
  `nums[mid:]` (Θ(n) time, not Θ(log n)).
- **Verified:** derivation ×2 + empirical timing (with a shared element so the refcount increments
  don't add cache misses) + tracemalloc peak
- **Retired:** —

## PY-07
- **Trick:** builtin-in-loop
- **Difficulty:** 3/3
- **Time:** Θ(n² log n)
- **Space:** Θ(n)
- **Why:** At iteration i, `sorted(seen)` copies and sorts i items in the general case: Θ(i log i).
  Σ i log i = Θ(n² log n). Space: `seen`, one `ordered` copy alive at a time, and `medians`, all Θ(n).
- **Common wrong answers:** Θ(n log n) (sees one sort and doesn't multiply by the loop). Θ(n²)
  (counts the copy or the loop but treats the sort as linear, so Partial only if the reasoning is about
  Timsort runs, see the probe). Θ(n²) space (counts every `ordered` ever made, but each is freed).
- **Probe questions:** "What if the code did `seen.append(x); seen.sort()` in place?" → `seen` is
  already sorted except for one element. Timsort finds the run and merges in Θ(i), so the total is
  Θ(n²). That's Timsort-specific; the generic bound is still n² log n. "Optimal running median?" →
  two heaps, O(n log n) total.
- **Variant seeds:** `if x > sum(window) / len(window)` inside a loop over a growing window. LC 724
  pivot index done with `sum(nums[:i]) == sum(nums[i+1:])` (Θ(n²) time, Θ(n) space from the slices).
- **Verified:** derivation ×2 + empirical timing (random input: n² log n beats n²; in-place probe:
  n²) + tracemalloc peak
- **Retired:** —

## PY-08
- **Trick:** pop-front
- **Difficulty:** 2/3
- **Time:** Θ(V²) worst case. O(V² + E) is also fine, and it equals O(V²) for simple graphs.
- **Space:** Θ(V)
- **Why:** `list.pop(0)` shifts every remaining element left (a memmove), so it costs O(len(queue)).
  On a star graph, the hub pushes V−1 nodes, and the pops then cost V−2, V−3, …, so Θ(V²). Scanning
  edges adds Θ(E). `v not in dist` is a dict lookup, O(1), so it's not a second trap. Space: `dist`
  and `queue` are O(V).
- **Common wrong answers:** Θ(V + E) (the textbook BFS bound, assuming `pop(0)` is O(1)). Θ(V·E)
  (makes up a cost for the dict check).
- **Probe questions:** "Fix?" → `collections.deque` with `popleft()`, which is O(1), restores
  Θ(V + E). "Best case for this list version?" → a path graph, where the queue length is always ≤ 1,
  so Θ(V + E).
- **Variant seeds:** build output in reverse with `res.insert(0, x)` (Θ(n²)). A sliding-window max
  that evicts with `window.pop(0)` (Θ(n·k)).
- **Verified:** derivation ×2 + empirical timing (star: n², with n² log n a close second because of
  memmove and cache effects; path: n) + tracemalloc peak
- **Retired:** —

## PY-09
- **Trick:** heapify-linear
- **Difficulty:** 3/3
- **Time:** Θ(n + k log n)
- **Space:** Θ(n)
- **Why:** The negating list comprehension is Θ(n). `heapq.heapify` is bottom-up sift-down. Most
  nodes sit near the leaves, and Σ (nodes at height h)·h = Θ(n), so heapify is Θ(n), not n log n. Each
  of the k `heappop`s costs O(log n). Space: the n-element heap copy, plus `top` (k ≤ n).
- **Common wrong answers:** Θ(n log n) (models heapify as n pushes; only correct when k = Θ(n)).
  Θ(k log n) (forgets the Θ(n) build). Θ(n log k) (confuses this with the size-k min-heap pattern).
  Θ(k) space (forgets the heap copy).
- **Probe questions:** "When does this become Θ(n log n)?" → when k = Θ(n). "Is building with n
  `heappush` calls the same?" → no, that's Θ(n log n) worst case (for example ascending pushes into a
  max-heap via negation).
- **Variant seeds:** `heapify(nums)` and then a single `heappop` to get the min (Θ(n)), compared with
  `sorted(nums)[0]` (Θ(n log n)). Merging k sorted lists with heapify on the k heads.
- **Verified:** derivation ×2 + op-count of comparisons on the bank code (k=1: n; k=16: n; k=n:
  n log n) + empirical timing at in-cache sizes (heapify alone and k=1: n) + tracemalloc peak. At
  sizes beyond the cache, wall-clock drifts above linear because of cache misses.
- **Retired:** —

## PY-10
- **Trick:** list-membership
- **Difficulty:** 1/3
- **Time:** Θ(n²)
- **Space:** Θ(n)
- **Best:** Θ(n)
- **Why:** `x not in unique` is a linear scan of a list. The list grows to d (the number of distinct
  values), so the time is Θ(n·d). Worst case all values are distinct: Θ(n²). Best case all values are
  equal: the list stays at size 1, so Θ(n). Space: `unique` holds d ≤ n items.
- **Common wrong answers:** Θ(n) worst case (treats `in` on a list like `in` on a set). Best Θ(1)
  (the loop still visits all n items).
- **Probe questions:** "Fix it but keep first-seen order." → a `seen` set next to the list, or
  `list(dict.fromkeys(nums))`, which is Θ(n). "Exactly what does the time depend on?" → n·d.
- **Variant seeds:** `if word in banned_list` inside a loop over text words (Θ(n·b)). Graph DFS with
  `visited = []` and `if v not in visited` (Θ(V² + E)).
- **Verified:** derivation ×2 + empirical timing (all distinct: n²; all equal: n) + tracemalloc peak
- **Retired:** —

## PY-11
- **Trick:** deepcopy-cost
- **Difficulty:** 2/3
- **Time:** Θ(m·r·c)
- **Space:** Θ(m·r·c), including the returned history (which the problem says counts).
- **Why:** `copy.deepcopy` walks the whole object graph: r row lists plus r·c cells, each with
  per-object dispatch and memo bookkeeping. So each call is Θ(r·c), and there are m calls. Each
  snapshot keeps r·c cells alive, so space is m·r·c.
- **Common wrong answers:** Θ(m) (treats deepcopy as O(1)). Θ(m·r) (thinks it copies only the
  row-pointer list, which is what `board.copy()` would do). Θ(r·c) space (forgets that every
  snapshot is kept).
- **Probe questions:** "Is `[row[:] for row in board]` asymptotically cheaper?" → no, it's also
  Θ(r·c), but with a much smaller constant (often 10× or more). "What would `board.copy()` cost, and
  what goes wrong?" → O(r), but the rows are shared, so every snapshot changes together.
- **Variant seeds:** backtracking (N-Queens or Sudoku) that `deepcopy`s the board at every recursive
  call. An undo stack that deep-copies a dict of lists after each edit.
- **Verified:** derivation ×2 + empirical timing (vs m: linear; vs side with r=c: side²) +
  tracemalloc peak (same)
- **Retired:** —

## PY-12
- **Trick:** slice-recursion
- **Difficulty:** 3/3
- **Time:** Θ(n²) (worst case, when s is a palindrome)
- **Space:** Θ(n²)
- **Why:** There are about n/2 calls. Each one makes `s[1:-1]`, a copy of length n−2, n−4, …, so
  Σ ≈ n²/4. Space: CPython has no tail-call elimination, and each suspended frame still holds its own
  `s`, so strings of length n, n−2, n−4, … are all alive at once. That's Θ(n²) characters, plus a
  Θ(n) stack.
- **Common wrong answers:** Θ(n) time ("n/2 calls, O(1) each" — the slice is a copy). Θ(n) space
  (counts only the stack depth, missing the copy each frame holds). Θ(n²) time with Θ(1) space
  (forgets the recursion entirely).
- **Grading note:** SPACE Θ(n) is a Miss only if the WHY treats slices as free. If they reason "each
  frame holds a slice" but then sum to Θ(n), that's a Miss with an arithmetic slip, and it's worth
  probing.
- **Probe questions:** "Rewrite with indices `lo, hi`." → Θ(n) time and Θ(n) stack, or Θ(1) as an
  iterative loop. "Best case?" → the first and last chars differ, so O(1).
- **Variant seeds:** recursive string reverse `return rev(s[1:]) + s[0]` (Θ(n²) time and space).
  Recursive `sum_list(nums) = nums[0] + sum_list(nums[1:])`.
- **Verified:** derivation ×2 + tracemalloc peak (n²) + op-count of copied chars (n²) + wall-clock
  fit t ≈ a·n + b·n². Per-call overhead is large, so the plain one-term ranking is borderline. At the
  largest size the n² term is most of the time.
- **Retired:** —

## PY-13
- **Trick:** builtin-in-loop
- **Difficulty:** 1/3
- **Time:** Θ(n²)
- **Space:** Θ(1)
- **Why:** The `max(nums)` in the condition is re-evaluated on every iteration, and each call is an
  O(n) scan. n iterations × Θ(n) = Θ(n²). There's no early exit, so the result holds for every input.
  `count` is the only auxiliary state.
- **Common wrong answers:** Θ(n) (reads `max(...)` as a cached value). Θ(n) space (assumes max
  builds a copy, but it streams).
- **Probe questions:** "Fix?" → hoist `m = max(nums)` above the loop, giving Θ(n), or use
  `nums.count(max(nums))`. "Is `max(a, b)` with two args O(n)?" → no, it's O(1) (the args are the
  "list").
- **Variant seeds:** `if x == min(nums) or x == sum(nums) // len(nums)` in a loop.
  `while sorted(arr) != arr:` with one swap per pass.
- **Verified:** derivation ×2 + empirical timing + tracemalloc peak
- **Retired:** —

## PY-14
- **Trick:** counter-cost
- **Difficulty:** 2/3
- **Time:** Θ((n−k+1)·k), which is O(n·k). That's Θ(n²) at k ≈ n/2.
- **Space:** Θ(k)
- **Why:** Each of the n−k+1 windows slices k chars (O(k)) and builds a `Counter` from them. Building
  a Counter iterates all k chars, so it's O(k), not O(1). The `==` compares two dicts, which is
  O(number of distinct keys) ≤ O(k). Space: one slice plus one window Counter (≤ min(k, σ) keys), and
  `need` is the same size, so Θ(k).
- **Common wrong answers:** Θ(n) (treats `Counter(...)` and `==` as O(1), the same as the
  sliding-window optimum). Θ(n·26) "because the alphabet is 26" (only `==` is bounded by σ; the slice
  and the Counter build are Θ(k)). Θ(n) space.
- **Probe questions:** "Get Θ(n)." → keep one Counter and slide it: add the incoming char, decrement
  the outgoing one, and track how many letters match (LC 438). "Cost of `Counter(s).most_common(1)`
  vs `.most_common()`?" → O(n + d) vs O(n + d log d).
- **Variant seeds:** `sorted(window) == sorted(p)` per window (Θ(n·k log k)). `Counter(a) - Counter(b)`
  rebuilt inside a loop over queries.
- **Verified:** derivation ×2 + empirical timing (k=n/4: n²; fixed n vs k: (n−k+1)·k) +
  tracemalloc peak vs k (linear, with both a 26-letter and an all-distinct alphabet)
- **Retired:** —

## PY-15
- **Trick:** constant-time-builtins
- **Difficulty:** 3/3
- **Time:** Θ(n)
- **Space:** Θ(n)
- **Why:** This is a reverse trap on time. `max(x, cur + x)` takes two arguments and does one
  comparison, O(1). It doesn't scan a list. Each loop iteration is O(1), so Θ(n). The space trap is
  the other way: `nums[1:]` runs once, but it allocates a full (n−1)-element copy that stays alive
  for the whole loop, so auxiliary space is Θ(n), not Θ(1).
- **Common wrong answers:** Θ(n²) time (pattern-matches `max` to the O(n) list scan). Θ(1) space
  (the textbook Kadane answer, which misses the slice copy). Θ(n²) time "because of the slice" (it
  happens once, not once per iteration).
- **Grading note:** TIME and SPACE are graded separately. Expect many learners to get TIME right and
  miss SPACE. Log the space miss under `slice-copy` in `past_mistakes`.
- **Probe questions:** "Make it truly O(1) space." → `for i in range(1, len(nums))`, or
  `itertools.islice(nums, 1, None)`. "What does `max(nums[i:])` cost inside a loop?" → O(n) per
  call, so Θ(n²).
- **Variant seeds:** `for x in sorted(nums):` once before a two-pointer loop (Θ(n log n) time, Θ(n)
  space). `while len(q) > 0 and q[-1] < x` in a monotonic stack (len is O(1), and the total is Θ(n)).
- **Verified:** derivation ×2 + empirical timing + tracemalloc peak
- **Retired:** —
