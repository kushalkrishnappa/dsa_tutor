# Bank Rules — complexity-analysis/

These rules extend dsa-tutor for this folder. Follow them on top of the normal SKILL.md flow.
Design rationale: `complexity-analysis/DESIGN.md`.

## Access grant (folder-local widening of the scope rule)

In this folder, you may read and write:
- the bank files: `deceptive_loops.py`, `recursion.py`, `python_costs.py`,
  `amortized_multivar.py`, `interview_set_1.py` … `interview_set_4.py`
- the hidden keys: `_keys/*.md`

Nothing here widens access outside `complexity-analysis/`.

**Never reveal key content before the learner has answered.** No quoting `Common wrong answers`,
no hinting at the `Trick` name, no difficulty. After grading, explain freely.

## Concepts = tricks

Each key entry has a `Trick` (kebab-case). In `progress.json`, one concept per trick; the concept
`name` is the trick slug. `topics` in the roadmap are the five groups (Deceptive Loops,
Recursion & Recurrences, Python Hidden Costs, Amortized & Multi-variable, Interview Sets).

## Session flow

1. Normal opening (warm-up, Band A, Band B) — use bank problems as question material.
2. **Pre-test** a new trick with 1–2 unseen problems carrying that `Trick`. Prefer Difficulty 1–2.
3. **Teach the gaps**: mental model, mnemonic, worked example, visual (recursion trees for RR,
   loop-count tables / sum diagrams for DL). Mnemonics must map onto code structure.
4. **Drill**: name problem IDs (e.g. "do DL-04 and DL-11"). Learner fills the answer block and
   says "grade". Interleave tricks and categories; never two problems with the same `Trick`
   back to back.
5. Interview sets come after the learner has drilled each snippet category at least once.

## Answer block

```
# TIME:
# SPACE:
# WHY:
# SURE:
```
Some problems also have `# ALSO: …` with extra slots (e.g. `# AMORTIZED:`, `# BEST:`). Grade every slot that exists. Interview problems are analyzed as written —
no optimization is asked for.

## Grading (interview-style), per slot

- ✅ **Pass** — tight bound (Θ-correct; O(...) wording is fine if it's the tight one) and sound
  reasoning in WHY.
- 🟡 **Partial** — right bound but WHY is missing/hand-wavy/wrong, **or** a valid-but-loose
  bound with otherwise good reasoning. Before finalizing, ask **one** probe question from the
  key's `Probe questions`; a strong answer upgrades to Pass.
- ❌ **Miss** — wrong bound. Name the specific misconception (use `Common wrong answers`),
  correct surgically with the key's derivation, and consider switching to teach mode for the trick.

Variables: accept equivalent forms (`O(n·m)` = `O(mn)`; `O(log n)` any base; `O(V+E)`).
Missing a variable that matters (answering `O(n)` for `Θ(n·k)`) is a Miss.

Space = auxiliary space (exclude the input; include the recursion stack, created copies,
and output only when the key says output counts). Keys state this explicitly when it matters.

## Recording (after every grade)

1. Append to the trick's concept in `progress.json`:
   ```json
   "bank_attempts": [
     {"id": "DL-07", "date": "YYYY-MM-DD",
      "time_ans": "…", "space_ans": "…", "why_ans": "…", "sure": true,
      "result": {"time": "pass", "space": "partial"}}
   ]
   ```
   Also append the ID to `practice_done` if not present.
2. Overall result = worst slot. **Partial counts as Wrong for scheduling.**
   Schedule via `SURE` (`y` = confident; `n` or blank = unsure) and the table in
   `references/progress_schema.md`. Wrong/Partial → `past_mistakes` entry phrasing the exact
   misconception; `high_confidence: true` if SURE was `y`.
3. **Reset the answer block** in the `.py` file to the blank slots (keep any `# ALSO:` prompt
   lines; blank only the answer lines).

## Re-exposure and variants

Count prior exposures of a problem ID = number of `bank_attempts` entries with that ID.
- 0 or 1 → reuse the problem.
- 2+ → write a variant instead: next free suffix (`DL-07b`, then `DL-07c`), built from the key's
  `Variant seeds`, same `Trick`, different surface. Append it to the end of the same `.py` file
  and add its key entry to the same `_keys/*.md`. Verify the key (derive twice; op-count it in
  the session scratchpad when runnable). Set the original's `Retired:` to
  `YYYY-MM-DD → DL-07b`. Retired problems are never served for review again.

## Do not

- Do not edit problem code except to reset answer blocks or append variants.
- Do not commit to git.
