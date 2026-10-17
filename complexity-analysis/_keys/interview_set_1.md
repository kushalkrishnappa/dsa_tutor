# Keys — interview_set_1.py (tutor only — learner does not open)

Conventions for this file: dict/set operations are expected O(1) **plus the cost of hashing the
key** (O(len) for a fresh str/tuple). SPACE is auxiliary: the input is excluded and the returned
value is excluded unless the problem statement says it counts. A learner who separately and
correctly states the output size gets credit for that too.

## IV-01
- **Trick:** multi-variable-bound
- **Secondary tricks:** hash-key-cost, slice-copy
- **Source:** LeetCode word-break
- **Hidden inefficiency:** none
- **Difficulty:** 3/3
- **Time:** Θ(n·L² + m·L). The n·L² part is the main loop; m·L is building `words` (hashing every
  dictionary word once). Assumes L ≤ n; in general the first term is n·min(n, L)².
- **Space:** Θ(n + m). That's `can` (n+1 bools), the set (m references — strings are not copied),
  and one temporary slice of ≤ L chars at a time.
- **Why:** For each `end` (n values) the inner loop tries ≤ L starts. Each try with `can[start]`
  true builds `s[start:end]`, a new string of length end−start, and hashes it for `in`. That's
  O(end−start). Lengths 1…L sum to ≈ L²/2, so each `end` costs Θ(L²) in the worst case. The
  worst case is s = "aaaa…", dict = {"a", "bbb…b" (length L)}. Every prefix is segmentable, and
  only the last start (length 1) matches, so the `break` never fires early.
- **Common wrong answers:** Θ(n²) or Θ(n³) (quotes the LeetCode editorial for the version whose
  inner loop runs over all starts; the `max(0, end − longest)` bound changes that). Θ(n·L) (treats
  the slice + set lookup as O(1), forgetting that a fresh slice must be copied and hashed). Θ(n·m)
  (pictures a loop over the dictionary words, which this code never does). Space Θ(n + m·L) (thinks
  `set()` copies the strings; it only stores references) — Partial, since it's a valid upper bound.
- **Probe questions:** "Why is `s[start:end] in words` O(end−start) and not O(1)?" → the slice is a
  new object; it must be copied and its hash computed from scratch before the table lookup (plus
  an O(len) equality check on a hit). "What does a trie over the dictionary buy you?" → from each
  reachable start, walk the trie forward ≤ L characters and mark every end where a word finishes:
  Θ(n·L + m·L).
- **Variant seeds:** top-down memo keyed on the suffix string `s[i:]` (n suffixes alive in the memo →
  Θ(n²) space); return all segmentations instead of a bool (output-sensitive, exponential).
- **Verified:** derivation ×2 + empirical op-count (vary n with L fixed → n; vary L with n fixed →
  L²; vary m with n, L fixed → m)
- **Retired:** —

## IV-02
- **Trick:** harmonic-sum
- **Secondary tricks:** multi-variable-bound
- **Source:** original
- **Hidden inefficiency:** none
- **Difficulty:** 2/3
- **Time:** Θ(n·log m), more precisely Θ(n(1 + log m)). Θ(n log n) when m = n.
- **Space:** Θ(n) (the `hits` array).
- **Why:** Server with interval p touches ⌊n/p⌋ seconds. The intervals are distinct, so the total
  ≤ n(1/1 + 1/2 + … + 1/m) = n·H_m ≈ n ln m. The worst case is intervals = 1..m. Allocating
  `hits` and the busiest-second scan add Θ(n). The outer loop adds Θ(m) ≤ Θ(n).
- **Common wrong answers:** Θ(n·m) (sees two nested loops and multiplies the bounds). Θ(n) (thinks
  each server is "about n/p, so constant per server", and forgets that the 1/p terms sum to log m).
  Θ(n log n) — Partial: a valid upper bound since m ≤ n, but it drops the variable that matters.
  Θ(m log n) (swaps the roles of the two variables).
- **Probe questions:** "What if the intervals didn't have to be distinct?" → m copies of interval 1
  give Θ(n·m). Distinctness is what makes the reciprocals a harmonic sum. "Why do intervals 1..m
  give the most work for a given m?" → Σ n/p over m distinct p is largest when the p are the m
  smallest values, 1..m, which gives n·H_m.
- **Variant seeds:** count, for every t ≤ n, how many of its divisors are in a set (same sieve shape);
  sieve of Eratosthenes, where marking only from primes gives Θ(n log log n).
- **Verified:** derivation ×2 + empirical op-count (vary n with m fixed → n; vary m with n fixed →
  log m)
- **Retired:** —

## IV-03
- **Trick:** list-membership
- **Secondary tricks:** permutations-enumeration, stack-depth-vs-total-calls
- **Source:** LeetCode permutations
- **Hidden inefficiency:** `if x in path` is a linear scan of a list. With a `used` boolean array
  or a set it would be O(1), giving the optimal Θ(n·n!).
- **Difficulty:** 3/3
- **Time:** Θ(n²·n!)
- **Space:** Θ(n) auxiliary (path + n+1 recursion frames). The output is Θ(n·n!) but isn't counted.
- **Why:** There are n!/(n−d)! nodes at depth d. Each internal node loops over all n values and runs
  `x in path` on a list of length d. That's ≈ d(n−d) for the misses plus d²/2 for the hits, so
  Θ(n·d). The depth n−1 level has n! nodes doing ≈ n²/2 work each, and the shallower levels shrink
  by factors of 2, 6, 24…, so the total is Θ(n²·n!). The n! leaves each copy `path[:]` (Θ(n·n!)),
  which is dominated.
- **Common wrong answers:** Θ(n·n!) (quotes the known optimal LeetCode bound, treating `in path` as
  O(1)). Θ(n!) (forgets both the per-node loop and the leaf copy). Θ(nⁿ) (thinks the loop over n
  values at n levels is never pruned) — a Miss, since the `continue` prunes and nⁿ/n! grows like eⁿ.
  Space Θ(n·n!) — accept only if the learner explicitly says they're counting the output.
- **Probe questions:** "Where exactly does the extra factor of n come from, and at which depth is
  most of it paid?" → `x in path` scans up to n−1 items, mostly at the last two levels, which hold
  n! nodes. "Change `path` to also maintain a set `used`. New time?" → Θ(n·n!).
- **Variant seeds:** permutations of a string with `ch not in cur` where `cur` is a str built by
  `cur + ch` (two hidden costs); k-permutations (P(n, k) leaves) with the same membership test.
- **Verified:** derivation ×2 + empirical op-count (exact comparisons counted; n = 3…9 fits n²·n!)
- **Retired:** —

## IV-04
- **Trick:** anagram-grouping
- **Secondary tricks:** hash-key-cost
- **Source:** LeetCode group-anagrams
- **Hidden inefficiency:** none
- **Difficulty:** 1/3
- **Time:** Θ(n·k log k)
- **Space:** Θ(n·k) (the dict keys: up to n distinct sorted strings of length k, plus the groups'
  n references).
- **Why:** For each of n strings: `sorted(s)` is Θ(k log k) comparisons. `"".join` builds a
  k-char key in Θ(k), and hashing that fresh key is Θ(k). The sort dominates. In the worst case
  every key is distinct, so the dict holds n keys of k chars each.
- **Common wrong answers:** Θ(n log n) (thinks the list of strings is being sorted). Θ(n·k)
  (forgets that sorting each string costs a log factor). Θ(n) (treats the dict operation as O(1)
  and the per-string work as constant). Space Θ(n) (counts dict entries but not the k characters
  inside each new key string).
- **Probe questions:** "Strings are lowercase a–z only. Can you beat k log k per string?" → yes: a
  26-count tuple as the key costs Θ(k) to build plus O(26) to hash: Θ(n·k) total. "Why is hashing
  the key not O(1)?" → it's a brand-new string; CPython computes its hash by reading all k chars
  (then caches it on that object).
- **Variant seeds:** key = `tuple(sorted(s))` (same bound, larger constant); group words by the
  multiset of their letters ignoring case and spaces (normalize, then sort).
- **Verified:** derivation ×2 + empirical op-count (comparison-counting wrapper; distinct-char words:
  vary k → k log k; vary n → n)
- **Retired:** —

## IV-05
- **Trick:** str-concat
- **Secondary tricks:** —
- **Source:** original
- **Hidden inefficiency:** `out = digits[i] + out` and `out = "," + out` *prepend*, so each one
  copies the whole current string. Appending chunks to a list and doing one `"".join(reversed(…))`
  (or slicing groups of 3) would be Θ(n).
- **Difficulty:** 2/3
- **Time:** Θ(n²)
- **Space:** Θ(n) (the current `out` and the new copy being built; old versions are freed)
- **Why:** The loop runs ≈ n + n/3 concatenations, and each one allocates a new string of length
  |out|+1 and copies the old contents. |out| grows to ≈ 4n/3, so the total copying is ≈ (4n/3)²/2 =
  Θ(n²). CPython's in-place concatenation trick only fires when the target variable is the *left*
  operand (`out = out + x` / `out += x`) and has no other references. Here `out` is the right
  operand, so it never applies.
- **Common wrong answers:** Θ(n) (treats string concatenation as O(1), or recalls that "CPython
  optimizes `+=`" without checking the operand order). Θ(n log n) (no basis — usually a guess).
  Space Θ(n²) (adds up all the intermediate strings, but each old one is freed once `out` is
  rebound).
- **Probe questions:** "What if the loop built `out = out + digits[i]` left to right instead?" → in
  CPython that usually runs in amortized Θ(n) because of the in-place resize optimization. It's an
  implementation detail, not a language guarantee, so `"".join` is still the portable answer.
  "Why doesn't the optimization apply here?" → it needs the existing string to be the left operand
  so it can be resized in place. Prepending always requires shifting the old contents.
- **Variant seeds:** build a binary representation with `bits = str(x % 2) + bits` (only log x
  digits — Θ(log² x)); reverse a string with `rev = ch + rev`.
- **Verified:** derivation ×2 + empirical op-count (chars copied fit n²) + timing of the real
  function in CPython 3.14 (fits n²; contrast `out = out + ch` fits n)
- **Retired:** —
