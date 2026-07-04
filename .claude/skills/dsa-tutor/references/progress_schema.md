# Progress File Schema (`dsa_progress.json`)

This file is the learner's memory across sessions. It is stored on disk and read/written automatically — the learner never downloads or uploads it. Read it at session start; write it after every checkpoint and at session end. Keep the structure below stable — append and update, don't restructure.

**Location:** `<project-root>/.dsa-tutor/dsa_progress.json`, where `<project-root>` is the nearest ancestor directory containing a `.claude/` folder (fall back to the current working directory).

## Top-level fields

- `learner_level` — string, e.g. `"intermediate"`.
- `last_session_date` — ISO date `YYYY-MM-DD`. Set to today on every write.
- `streak` — integer count of distinct days studied (increment when today differs from the previous `last_session_date`).
- `curriculum` — object keyed by **area** (e.g. `"graphs"`, `"trees"`, `"dynamic-programming"`). Each area object:
  - `roadmap` — path to the generated roadmap HTML, e.g. `".dsa-tutor/roadmaps/graphs.html"`.
  - `topics` — ordered array of `{ "name": string, "status": "not-started" | "in-progress" | "done" }`.
  - `current` — name of the topic currently in progress (or `null`).
- `concepts` — array of concept-tracking objects:
  - `name` — e.g. `"Breadth-First Search"`.
  - `area` — the area this concept belongs to, e.g. `"graphs"`.
  - `mental_model` — the anchor image used (so refreshers reuse it).
  - `mnemonic` — the sticky hook taught for this concept.
  - `mastery` — `"learning" | "shaky" | "solid"`.
  - `last_reviewed` — ISO date.
  - `review_interval` — integer days until next review (Leitner: 1 → 3 → 7 → 16 → 30; reset to 1 on a miss).
  - `aces` — integer count/streak of clean correct answers for this concept.
  - `past_mistakes` — array of strings: the exact misconceptions the learner has made, phrased so they can be re-tested. Keep these; they feed targeted quizzes.
  - `visual` — path to the generated interactive HTML for this concept, e.g. `".dsa-tutor/visuals/bfs.html"` (or `null`).
  - `practice_done` — array of solved problem identifiers, e.g. `["LC-200", "HR-bfs-shortest-reach"]`.
- `notes` — freeform string for anything useful next session (learner language preference, current sub-topic, etc.).

## "Due for review" computation

A concept is due when `today - last_reviewed >= review_interval` (in days). Surface due concepts first in the refresh and the Daily Quick Quiz.

## Example

```json
{
  "learner_level": "intermediate",
  "last_session_date": "2026-06-27",
  "streak": 4,
  "curriculum": {
    "graphs": {
      "roadmap": ".dsa-tutor/roadmaps/graphs.html",
      "current": "Breadth-First Search",
      "topics": [
        { "name": "Graph Terminology", "status": "done" },
        { "name": "Graph ADT", "status": "done" },
        { "name": "Representations", "status": "done" },
        { "name": "Breadth-First Search", "status": "in-progress" },
        { "name": "Depth-First Search", "status": "not-started" }
      ]
    }
  },
  "concepts": [
    {
      "name": "Breadth-First Search",
      "area": "graphs",
      "mental_model": "A wave spreading out one ring at a time from the start node.",
      "mnemonic": "BFS = Breadth = a queue; you serve neighbors in arrival order.",
      "mastery": "shaky",
      "last_reviewed": "2026-06-27",
      "review_interval": 1,
      "aces": 1,
      "past_mistakes": [
        "Used a stack instead of a queue, which turns BFS into DFS."
      ],
      "visual": ".dsa-tutor/visuals/bfs.html",
      "practice_done": ["LC-200"]
    },
    {
      "name": "Binary Search",
      "area": "searching",
      "mental_model": "Phone book: open the middle, throw away the wrong half.",
      "mnemonic": "Halve it 'til you have it -> log n.",
      "mastery": "solid",
      "last_reviewed": "2026-06-25",
      "review_interval": 7,
      "aces": 4,
      "past_mistakes": [],
      "visual": null,
      "practice_done": ["LC-704", "LC-35"]
    }
  ],
  "notes": "Prefers Python. Mid-way through graph traversals; next: DFS trigger patterns."
}
```
