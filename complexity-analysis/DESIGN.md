# Complexity Analysis Problem Bank — Design

Date: 2026-10-14 · Status: approved in brainstorming, awaiting spec review

## Goal

Build a practice bank of ~80 Python problems for drilling *eccentric* time/space complexity
analysis of the kind that shows up in coding interviews. The bank is studied through the existing
`dsa-tutor` skill (pre-test → teach gaps → drill → spaced review), with Claude grading the
learner's answers interview-style against hidden answer keys.

## Decisions (from brainstorming)

| Topic | Decision |
|---|---|
| Deliverable | Practice problem bank |
| Categories | Deceptive loops · Recursion & recurrences · Python hidden costs · Amortized & multi-variable |
| Problem form | Tiered: abstract snippets first, then realistic interview code |
| Answer scope | Time + space + short justification |
| Case analysis | Worst case by default; best/avg/amortized asked only on problems where it matters |
| Checking | Claude grades |
| Answer keys | Stored in the repo, in a hidden file the learner agrees not to open |
| Where learner answers | Comment block under each problem in the `.py` file |
| Confidence | `# SURE: y/n` slot in every answer block (feeds dsa-tutor's confidence-weighted schedule) |
| Progress | `dsa-tutor` `progress.json` (spaced repetition) |
| Re-attempts | Block cleared after grading; fresh variant once a problem has been seen 2+ times |
| Size | Large: ~60 snippets (~15/category) + ~20 interview problems |
| Ordering | Shuffled difficulty within each file |
| Difficulty labels | Not shown; recorded only in keys |
| Snippet layout | One file per category |
| Interview layout | A few sets of ~5 problems, mixed tricks |
| Interview source | ~Half LeetCode-linked, ~half original |
| Interview code quality | Mix of optimal and subtly inefficient; learner analyzes what's written |
| Runnable? | Pseudocode-ish allowed (`do_constant_work()` etc.) |
| Grading strictness | Interview-style (tight bound expected, partial credit, probe follow-ups) |
| Teaching | `dsa-tutor` normal flow: pre-test then teach |
| Folder | `complexity-analysis/` |
| Key location | `complexity-analysis/_keys/*.md` |
| Variants | Written on demand at review time |
| Integration approach | **A** — topic-local `bank_rules.md` + one-line generic hook in `dsa-tutor` `SKILL.md` |
| Git | Claude does not commit; learner commits their own work |

## 1. Layout

```
complexity-analysis/
├── DESIGN.md                 # this file
├── deceptive_loops.py        # DL — ~15 snippets
├── recursion.py              # RR — ~15 snippets
├── python_costs.py           # PY — ~15 snippets
├── amortized_multivar.py     # AM — ~15 snippets
├── interview_set_1.py        # IV — ~5 realistic problems each, tricks mixed
├── interview_set_2.py
├── interview_set_3.py
├── interview_set_4.py
├── _keys/                    # hidden — learner does not open
│   ├── deceptive_loops.md
│   ├── recursion.md
│   ├── python_costs.md
│   ├── amortized_multivar.md
│   └── interview_set_1.md … interview_set_4.md
└── .dsa-tutor/
    ├── bank_rules.md         # how the tutor runs this bank
    ├── progress.json         # created by dsa-tutor New-Area Setup
    └── roadmap.html          # created by dsa-tutor
```

### Problem IDs

`DL-01…`, `RR-01…`, `PY-01…`, `AM-01…`, `IV-01…`. IDs are stable, never reused, and assigned
in authoring order (not difficulty order), so numbering leaks no difficulty signal. Variants take
a letter suffix: `DL-07b`, `DL-07c`.

### Problem format

```python
# ─── DL-07 ───────────────────────────────────────────
# n = len(nums)
def dl07(nums):
    n = len(nums)
    i = 1
    while i < n:
        for j in range(0, n, i):
            do_constant_work()
        i *= 2

# TIME:
# SPACE:
# WHY:
# SURE:
```

Rules:
- A variables line (`# n = …, k = …`) precedes the code whenever more than one size matters, or
  whenever "n" would otherwise be ambiguous.
- Where case analysis matters, an extra prompt line and slot appear, e.g.
  `# ALSO: amortized cost per push()` followed by `# AMORTIZED:`.
- Placeholder helpers are allowed. A placeholder is O(1) unless its cost is stated in a comment.
- Snippet functions are plain functions named after their ID (`dl07`).
- Interview problems open with a docstring holding the problem statement (and the LeetCode URL for
  LeetCode-based ones), then a plain function — never a `class Solution` wrapper — then the same
  answer block.
- Problems within a file are ordered with difficulty shuffled.

## 2. Answer key format (`_keys/<file>.md`)

One `##` section per problem:

```markdown
## DL-07
- **Trick:** geometric-inner-loop
- **Difficulty:** 3/3
- **Time:** Θ(n)
- **Space:** Θ(1)
- **Why:** Inner loop does n/i steps; i = 1, 2, 4, … so total = n(1 + 1/2 + 1/4 + …) < 2n.
  The outer loop's log n passes do not multiply because each pass shrinks geometrically.
- **Common wrong answers:** O(n²) (sees nested loops); O(n log n) (multiplies log n passes × n).
- **Probe questions:** "What if `i += 1` instead of `i *= 2`?" → harmonic sum, Θ(n log n).
- **Variant seeds:** step `i *= 3`; inner loop `range(i)` instead of `range(0, n, i)`.
- **Verified:** derivation ×2 + empirical op-count
- **Retired:** —
```

Field purposes:
- **Trick** — the concept name in `progress.json`; mastery and review are tracked per trick, not
  per problem. Trick names are kebab-case and shared across problems that test the same idea.
- **Difficulty** — 1–3, hidden from the learner; used to pick pre-test items and weight review.
- **Common wrong answers** / **Probe questions** — drive partial credit and follow-ups.
- **Variant seeds** — starting points for on-demand variants.
- **Verified** — either `derivation ×2 + empirical op-count` or `derivation ×2` (for
  recurrences/pseudocode that can't be run meaningfully).
- **Retired** — the date and replacing variant ID once a problem is retired from review.

## 3. Grading and review flow (`.dsa-tutor/bank_rules.md`)

`bank_rules.md` contains the operational version of this section for the tutor to follow.

### Session flow
1. **Pre-test** a trick with 1–2 unseen bank problems.
2. **Teach gaps** using dsa-tutor's normal tools (mental model, mnemonic, worked example,
   visuals — e.g. recursion-tree visuals for RR). Mnemonics must map to code structure.
3. **Drill**: the tutor names problem IDs; the learner fills answer blocks and says "grade".
4. **Review**: due tricks are interleaved per dsa-tutor's spaced-repetition schedule.

### Grading (interview-style), per slot (TIME, SPACE, and any ALSO slot)
- ✅ **Pass** — tight bound and sound reasoning.
- 🟡 **Partial** — right bound with shaky/missing reasoning, or a loose-but-valid bound with good
  reasoning. Ask one probe question from the key before finalizing.
- ❌ **Miss** — wrong bound. Correct it surgically, naming the specific misconception from the
  key's common wrong answers; dsa-tutor may switch to teach mode for that trick.

### Recording
After grading, append to the trick's concept in `progress.json`:

```json
"bank_attempts": [
  {"id": "DL-07", "date": "2026-10-15",
   "time_ans": "O(n log n)", "space_ans": "O(1)", "why_ans": "…", "sure": true,
   "result": {"time": "miss", "space": "pass"}}
]
```

Misses are also added to `past_mistakes` as dsa-tutor already does. Then the answer block in the
`.py` file is reset to blank (`# TIME:` / `# SPACE:` / `# WHY:` / `# SURE:` and any ALSO slot). The `SURE`
value plus the overall result (worst slot wins) picks the row in dsa-tutor's confidence-weighted
schedule; a blank `SURE` counts as unsure. For scheduling, **Partial counts as Wrong**: reset the
interval to 1 and log a `past_mistakes` entry (`high_confidence: true` if `SURE` was `y`).

### Re-exposure
- Seen once → reuse the original problem (its block is already blank).
- Seen 2+ times → write a fresh variant from the key's variant seeds (`DL-07b`), add it to the
  same `.py` file and key file (verified like any other problem), and mark the original
  `Retired` in its key.

### dsa-tutor hook
Add one generic instruction to `.claude/skills/dsa-tutor/SKILL.md`:

> If the active folder's `.dsa-tutor/bank_rules.md` exists, read it at session start and follow
> it. It may grant read access to additional files in the active folder (e.g. `_keys/`).

`bank_rules.md` grants the tutor read/write access to `complexity-analysis/_keys/` and the bank
`.py` files. This is a deliberate, folder-local widening: the existing scope rule limits progress
I/O to the active folder's `.dsa-tutor/` (plus the learner's own code files), and the grant never
reaches outside `complexity-analysis/`.

## 4. Content plan

### Trick coverage (~15 problems per category; some tricks appear twice in different disguises)

**DL — Deceptive loops:** geometric inner loop (Θ(n)) · harmonic sum (Θ(n log n)) ·
`i*i < n` (Θ(√n)) · `i = i*i` (Θ(log log n)) · two-pointer nested while (Θ(n)) · sliding-window
inner while (Θ(n)) · triangular `j < i` (Θ(n²)) · `i < j < k` (Θ(n³)) · early `break` (worst
case still counts) · loops over different sizes (Θ(n·m)) · inner log i (log n! = Θ(n log n)) ·
iterating divisors · halving `while` inside a `for`.

**RR — Recursion & recurrences:** naive fib (Θ(φⁿ)) · memoized fib · T(n)=2T(n/2)+1 → Θ(n) ·
merge sort · T(n-1)+n → Θ(n²) · T(n/2)+n → Θ(n) · T(n/3)+T(2n/3)+n → Θ(n log n) · 3-way
branching · stack depth vs total calls (space) · T(√n)+1 → Θ(log log n) · Master Theorem case 3 ·
subsets (Θ(n·2ⁿ)) · permutations (Θ(n·n!)) · 2D memo state.

**PY — Python hidden costs:** slicing in a loop · `in` on list vs set · `str +=` (including the
CPython in-place optimization caveat) · `pop(0)`/`insert(0)` vs `deque` · `sorted()`/`max()`/
`sum()` inside a loop · `path + [x]` in recursion · `s[1:]` recursion · hashing tuple/string keys
costs O(k) · `list.index` · `heapify` is O(n) · `deepcopy` · `Counter`.

**AM — Amortized & multi-variable:** dynamic array append · two-stack queue · monotonic stack ·
union-find (α(n)) · grid BFS O(m·n) · adjacency list O(V+E) vs matrix O(V²) · Dijkstra
O((V+E) log V) · anagram grouping O(n·k log k) · trie O(total chars) · word search O(m·n·3ᴸ) ·
binary search on the answer O(n log R) · top-k heap O(n log k).

**IV — Interview sets (4 × ~5):** ~10 LeetCode-linked, ~10 original. ~8 of the 20 contain a
hidden inefficiency (e.g. correct solution with a slice or `in list` inside a loop). Each set
mixes tricks from all four categories.

### Verification (every key, before it enters the bank)
1. **Two independent derivations** — derive, then re-derive from scratch; resolve any
   disagreement before writing the key.
2. **Empirical op-count where feasible** — a runnable copy goes in Claude's session scratchpad (not
   the repo); count operations over growing n and confirm the growth matches the key.
   Recurrence-only and pseudocode-only problems are marked `derivation ×2`.

### Build order
1. `.dsa-tutor/bank_rules.md` + the `SKILL.md` hook.
2. One category at a time, each as `.py` file + `_keys/*.md` with every key verified: DL → RR →
   PY → AM.
3. Interview sets 1–4.

`progress.json` and `roadmap.html` are not hand-built; dsa-tutor creates them through its normal
New-Area Setup on the first session in `complexity-analysis/`.

## Out of scope
- Runnable test harnesses or timing tools in the repo (the empirical check is Claude-side only).
- Self-grading answer reveals.
- Changes to dsa-tutor beyond the one-line hook.
- Git commits.
