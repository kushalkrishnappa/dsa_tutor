# DSA Tutor — generic, persistent, visual tutor (design)

**Date:** 2026-06-27
**Status:** Approved (brainstorming complete)
**Scope:** Rework the existing `dsa-tutor` skill into a fully functional, persistent, visual Socratic tutor that works for **any** DSA topic.

---

## 1. Problem & goals

The current `dsa-tutor` skill teaches DSA Socratically and tracks progress in a `dsa_progress.json` file, but the learner must **download and re-upload** that file every session. The skill also only describes a teaching *method* — it has no concrete mechanism for persistence, visualizations, a topic roadmap, guided implementation, or curated practice.

Goals:

1. **Auto-persist progress** to disk under `.dsa-tutor/` — no manual download/upload.
2. **Generic across all of DSA** — no hard-coded topic content. Graphs is only an example of what the engine produces at runtime.
3. **Unforgettable visual teaching** — generate interactive HTML visualizations ("moving parts") with embedded questions.
4. **Generated topic roadmap** — a clean prerequisite map for whatever area the learner studies.
5. **Guided Python implementation** — in the learner's own project files, reviewed by the tutor.
6. **Curated practice problems** — recommended per topic (LeetCode / HackerRank / dsapanicle.com), recorded per learner.
7. **Multi-day mastery tracking** — record where the learner aces vs. slips; re-drill exactly the misses via spaced repetition.

Non-goals: a pre-built static problem bank for all of DSA; storing the learner's solution code inside `.dsa-tutor/` (it lives in their own files); any graph-specific shipped content.

---

## 2. Key decisions (from brainstorming)

| Decision | Choice | Notes |
|---|---|---|
| Storage location | Project-root `./.dsa-tutor/` | Found when working inside the project; directory containing `.claude/`, falling back to cwd. |
| Save timing | Continuously **and** at session end | Write after each checkpoint so an abrupt close never loses progress. |
| Visual delivery | Generated self-contained interactive HTML files | Saved to `.dsa-tutor/visuals/`; persist for revisiting. |
| Scope | General DSA engine | No topic-specific shipped content; graphs is an example only. |
| Practice problems | Recommended on demand from the tutor's DSA knowledge, recorded per learner | Supersedes the earlier "static reference file" idea (impractical across all DSA). |
| Diagnostic depth | Adaptive; stop when level is clear (≈2–5 questions) | One question at a time. |
| Advanced topics | Included as a "stretch" tier in generated roadmaps | Rendered distinctly (dashed). |

---

## 3. On-disk runtime layout (generic, created automatically)

```
<project-root>/.dsa-tutor/
  dsa_progress.json     # the learner's memory across sessions — auto read & written
  roadmaps/             # generated per area: graphs.html, trees.html, dynamic-programming.html …
  visuals/              # generated per concept: bfs.html, quicksort.html, dp-knapsack.html …
```

- **Project root** = the directory containing `.claude/`; if that cannot be determined, use the current working directory.
- The tutor creates `.dsa-tutor/` and subdirectories on first write. No setup required from the learner.
- The learner's **implementation code stays in their own project files** (e.g., `graphs/graphs.py`); the tutor reads and reviews those, and never relocates them.

---

## 4. Skill package layout (`.claude/skills/dsa-tutor/`) — all generic

```
SKILL.md                       # rewritten orchestration
references/
  progress_schema.md           # renamed from the misspelled "preogress_schema.md"; expanded, generic
  visual_authoring.md          # reusable HTML template + drawing helpers for ANY DSA shape, and the roadmap generator
```

### SKILL.md responsibilities
- Session lifecycle (start / during / end).
- The per-topic teaching cycle (below).
- Adaptive diagnostic protocol.
- Existing teaching method (mental model → mnemonic → application → one-question-at-a-time → surgical correction → coding fluency) — retained.
- Roadmap generation instruction (delegates rendering details to `visual_authoring.md`).
- Practice-recommendation instruction.
- Mastery tracking + spaced repetition.
- Frontmatter `description` updated so **auto-persistence is primary** and an uploaded file is a legacy fallback.

### references/visual_authoring.md responsibilities
A generic guide for generating two kinds of artifact as **self-contained HTML** (inline CSS/JS, no external dependencies), written with the Write tool into `.dsa-tutor/`:

1. **Concept visuals** (`visuals/<concept>.html`): an animation of the algorithm/structure with play / pause / step controls and 1–2 embedded "predict the next step" questions. Includes reusable drawing helpers for the common DSA shapes: **graphs, trees, arrays/grids, linked lists, stacks/queues, recursion trees, DP tables**.
2. **Roadmap maps** (`roadmaps/<area>.html`): a clean prerequisite DAG using the validated style — centered foundations spine, right-angle (orthogonal) connectors, phase labels down the left, solid = prerequisite / dashed = next phase, "start here" highlighting.

The graph BFS visual and graph roadmap built during brainstorming are reference examples of this style, not shipped files.

---

## 5. The per-topic cycle (generic; repeats for any concept in any area)

1. **Diagnose** — adaptive questions, one at a time, until the learner's level on this topic is clear.
2. **Teach unforgettably** — mental model → mnemonic → precise definition → "when to reach for it" trigger.
3. **Visualize** — generate `.dsa-tutor/visuals/<concept>.html`; tell the learner to open it; ask guiding questions tied to the visualization.
4. **Implement in Python** — learner writes/traces code in their own files; tutor reviews and highlights recurring idioms.
5. **Practice** — recommend topic-appropriate problems (LeetCode / HackerRank / dsapanicle.com); record them.
6. **Track & save** — update mastery / mnemonic / mistakes / aces / review interval; save immediately.
7. **Advance** — regenerate/update the area roadmap (status colors), then pick the next available topic.

---

## 6. Session lifecycle

- **Start:** Read `.dsa-tutor/dsa_progress.json` with the Read tool.
  - If present → **Returning-Learner Refresh**: last topic + how it went, mnemonics for shaky items, "due for review today," then offer the Daily Quick Quiz.
  - If absent but the learner uploaded/pasted a legacy `dsa_progress.json` → **import it once** by writing it to the new path.
  - If neither → **First-Session Setup** (brief how-it-works, then diagnostic).
- **During:** Save after each checkpoint (concept taught/updated, quiz graded, practice recorded).
- **End:** Final save; one-line reminder of what's due next time. No download/upload language anywhere.

---

## 7. Progress schema (expanded, generic)

Keep the existing fields; add area-awareness and richer per-concept tracking. Full schema and a worked example live in `references/progress_schema.md`. Summary of additions:

- **`curriculum`** — keyed by **area** (e.g., `"graphs"`, `"dynamic-programming"`). Each area holds:
  - `roadmap` — path to the generated roadmap HTML.
  - `topics` — ordered list with per-topic `status` (`not-started` | `in-progress` | `done`).
  - `current` — the topic in progress.
- **Per concept (existing `concepts[]` objects), add:**
  - `area` — which area it belongs to.
  - `aces` — count/streak of clean correct answers.
  - `visual` — path to its generated HTML, if any.
  - `practice_done` — list of solved problem identifiers (e.g., `"LC-200"`, `"HR-bfs-shortest-reach"`).
- **Unchanged:** `learner_level`, `last_session_date`, `streak`, per-concept `name` / `mental_model` / `mnemonic` / `mastery` / `last_reviewed` / `review_interval` / `past_mistakes`, and `notes`.

Spaced repetition unchanged: Leitner 1 → 3 → 7 → 16 → 30 days; reset to 1 on a miss. "Due" when `today - last_reviewed >= review_interval`.

---

## 8. Mastery tracking ("where I aced / where I went wrong")

- Every graded answer updates the concept:
  - **Correct** → bump `review_interval` (next Leitner step), increment `aces`, possibly raise `mastery`.
  - **Wrong** → reset `review_interval` to 1, append the **exact misconception** to `past_mistakes`, flag it, lower `mastery`.
- The **Daily Quick Quiz** preferentially pulls from `past_mistakes` + due items, reminding the relevant mnemonic each time — so the tutor keeps re-testing precisely what the learner tends to miss.

---

## 9. Cleanups bundled in

- Rename `references/preogress_schema.md` → `references/progress_schema.md` so SKILL.md's pointer resolves (currently broken).
- Remove "regenerate and present for download" / "remind to upload" language from both SKILL.md and the schema doc.
- Verify the `dsapanicle.com` URL/scheme when wiring up practice recommendations; fall back gracefully if a topic page can't be confirmed.

---

## 10. Out of scope / future

- Pre-built static problem banks per topic.
- Auto-running or grading the learner's Python (tutor reviews by reading; it does not execute solutions as part of the cycle).
- Non-DSA subjects.
