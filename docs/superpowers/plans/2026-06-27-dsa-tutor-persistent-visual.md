# DSA Tutor — Persistent, Visual, Generic Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Use superpowers:writing-skills when editing the skill files. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rework the `dsa-tutor` skill into a generic, fully functional Socratic tutor that auto-persists progress to `.dsa-tutor/`, teaches with generated interactive visualizations, generates per-area roadmaps, recommends practice problems, and tracks mastery across days — with no topic-specific content shipped.

**Architecture:** Three skill files. `references/progress_schema.md` defines the persisted JSON memory. `references/visual_authoring.md` provides a reusable self-contained HTML template + drawing helpers (graphs, arrays/grids, trees, linked lists) and the roadmap-map generator. `SKILL.md` orchestrates: read/write `.dsa-tutor/` on disk, run the per-topic cycle, generate roadmaps and visuals, recommend practice, and track mastery via spaced repetition. All artifacts are generated at runtime; nothing graph-specific is shipped.

**Tech Stack:** Markdown skill files; generated artifacts are self-contained HTML/CSS/JS (no external dependencies). Verification uses `grep`, `ls`, `python3 -m json.tool`, and HTML self-containment checks.

**Environment notes:** Not a git repository — "Commit" steps are replaced by verification checkpoints. Spec: [docs/superpowers/specs/2026-06-27-dsa-tutor-design.md](docs/superpowers/specs/2026-06-27-dsa-tutor-design.md).

---

## File Structure

| File | Responsibility | Action |
|---|---|---|
| `.claude/skills/dsa-tutor/references/preogress_schema.md` | (misspelled) progress schema | **Rename → delete** |
| `.claude/skills/dsa-tutor/references/progress_schema.md` | Generic, area-aware persisted-memory schema + example | **Create (from rename) + expand** |
| `.claude/skills/dsa-tutor/references/visual_authoring.md` | Reusable HTML template, drawing helpers, roadmap generator | **Create** |
| `.claude/skills/dsa-tutor/SKILL.md` | Orchestration: lifecycle, per-topic cycle, roadmaps, visuals, practice, mastery | **Rewrite** |

Runtime artifacts (created by the tutor at runtime, not by this plan): `<project-root>/.dsa-tutor/dsa_progress.json`, `<project-root>/.dsa-tutor/roadmaps/*.html`, `<project-root>/.dsa-tutor/visuals/*.html`.

---

## Task 1: Rename + expand the progress schema reference

**Files:**
- Delete: `.claude/skills/dsa-tutor/references/preogress_schema.md`
- Create: `.claude/skills/dsa-tutor/references/progress_schema.md`

- [ ] **Step 1: Verify the broken state (the "failing test")**

Run:
```bash
ls /Users/kushalkrishnappa/Playground/dsa/.claude/skills/dsa-tutor/references/
grep -n "progress_schema.md" /Users/kushalkrishnappa/Playground/dsa/.claude/skills/dsa-tutor/SKILL.md
```
Expected: only `preogress_schema.md` exists (misspelled), but `SKILL.md` references `progress_schema.md` → broken link confirmed.

- [ ] **Step 2: Rename the file**

Run:
```bash
git_dir=/Users/kushalkrishnappa/Playground/dsa/.claude/skills/dsa-tutor/references
mv "$git_dir/preogress_schema.md" "$git_dir/progress_schema.md"
ls "$git_dir"
```
Expected: `progress_schema.md` present, `preogress_schema.md` gone.

- [ ] **Step 3: Replace the file content with the expanded, generic schema**

Overwrite `.claude/skills/dsa-tutor/references/progress_schema.md` with exactly:

````markdown
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
````

- [ ] **Step 4: Verify the example JSON is valid (the "passing test")**

Run:
```bash
python3 - <<'PY'
import re, json, pathlib
text = pathlib.Path("/Users/kushalkrishnappa/Playground/dsa/.claude/skills/dsa-tutor/references/progress_schema.md").read_text()
block = re.search(r"```json\n(.*?)\n```", text, re.S).group(1)
json.loads(block)
print("OK: example JSON parses")
PY
```
Expected: `OK: example JSON parses`.

- [ ] **Step 5: Verify download/upload language is gone**

Run:
```bash
grep -ni "download\|re-upload\|present it for download" /Users/kushalkrishnappa/Playground/dsa/.claude/skills/dsa-tutor/references/progress_schema.md || echo "CLEAN"
```
Expected: `CLEAN`.

---

## Task 2: Create the visual authoring reference

**Files:**
- Create: `.claude/skills/dsa-tutor/references/visual_authoring.md`

- [ ] **Step 1: Verify it does not yet exist (the "failing test")**

Run:
```bash
ls /Users/kushalkrishnappa/Playground/dsa/.claude/skills/dsa-tutor/references/visual_authoring.md 2>/dev/null || echo "MISSING"
```
Expected: `MISSING`.

- [ ] **Step 2: Create the file**

Create `.claude/skills/dsa-tutor/references/visual_authoring.md` with exactly:

````markdown
# Visual Authoring Guide

How to generate the two visual artifacts the tutor uses. Both are **self-contained HTML** — inline CSS/JS, no external `src`/`href`, no CDNs — written with the Write tool so they work offline and persist for the learner to revisit.

- **Concept visuals** → `<project-root>/.dsa-tutor/visuals/<concept>.html` (slug the concept name, e.g. `breadth-first-search` → `bfs.html`).
- **Roadmap maps** → `<project-root>/.dsa-tutor/roadmaps/<area>.html`.

Create the directory on first write. Tell the learner to open the file (e.g. `file://<absolute-path>` or via the IDE).

---

## Part A — Concept visual template

A concept visual is an animation with play / pause / step / prev / reset controls, a narration line, and 1–2 embedded "predict the next step" questions. You only customize the title, description, and the `buildSteps()` function; everything else is fixed infrastructure.

`buildSteps()` returns an array of step objects:
- `draw` — a function that renders this frame using a drawing helper.
- `note` — narration string for this frame.
- `question` (optional) — `{ prompt, options: [...], answer: <index>, explain }`. The animation can be paused here so the learner predicts before revealing.

Copy this whole file, replace `__TITLE__`, `__DESCRIPTION__`, and `buildSteps()`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>__TITLE__</title>
<style>
  body{margin:0;background:#15151f;color:#eee;font:15px/1.5 -apple-system,Segoe UI,Roboto,sans-serif}
  .wrap{max-width:760px;margin:0 auto;padding:24px}
  h1{font-size:20px;margin:0 0 4px}
  .desc{color:#aaa;margin:0 0 16px}
  #stage{background:#1d1d2a;border:1px solid #333;border-radius:10px}
  svg{width:100%;height:auto;display:block}
  .narration{min-height:24px;margin:12px 0;color:#cfcfe0}
  .controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
  button{background:#2b2b3a;color:#eee;border:1px solid #555;border-radius:6px;padding:6px 12px;cursor:pointer}
  button:hover{border-color:#e0b341}
  .counter{margin-left:auto;color:#888}
  .quiz{margin-top:16px;background:#1d1d2a;border:1px solid #3a3a4a;border-radius:10px;padding:14px}
  .quiz .q{font-weight:600;margin-bottom:8px}
  .quiz button{margin:4px 6px 4px 0}
  .reveal{margin-top:10px;color:#cfcfe0}
</style>
</head>
<body>
<div class="wrap">
  <h1>__TITLE__</h1>
  <p class="desc">__DESCRIPTION__</p>
  <div id="stage"><svg id="svg" viewBox="0 0 640 360"></svg></div>
  <div class="narration" id="narration">—</div>
  <div class="controls">
    <button id="prev">◀ Prev</button>
    <button id="play">▶ Play</button>
    <button id="step">Step ▶|</button>
    <button id="reset">⟲ Reset</button>
    <label>Speed <input id="speed" type="range" min="300" max="1600" value="850"></label>
    <span class="counter" id="counter"></span>
  </div>
  <div class="quiz" id="quiz" hidden>
    <div class="q" id="qtext"></div>
    <div id="qopts"></div>
    <div class="reveal" id="reveal" hidden></div>
  </div>
</div>
<script>
/* ===== infrastructure: drawing helpers ===== */
const SVG="http://www.w3.org/2000/svg";
const svg=document.getElementById('svg');
function el(t,a){const e=document.createElementNS(SVG,t);for(const k in a)e.setAttribute(k,a[k]);return e;}
function clear(){while(svg.firstChild)svg.removeChild(svg.firstChild);}
const COL={idle:'#2b2b3a',idleStroke:'#666',visited:'#3fb950',current:'#e0b341',curStroke:'#ffd75e',edge:'#7a7a8c',text:'#fff'};

// graph: {nodes:[{id,x,y,label}], edges:[[a,b]], visited:Set, current:id}
function drawGraph(g){
  clear(); const pos={}; g.nodes.forEach(n=>pos[n.id]=n);
  (g.edges||[]).forEach(([a,b])=>svg.appendChild(el('line',
    {x1:pos[a].x,y1:pos[a].y,x2:pos[b].x,y2:pos[b].y,stroke:COL.edge,'stroke-width':2})));
  g.nodes.forEach(n=>{
    const v=g.visited&&g.visited.has(n.id), c=g.current===n.id;
    svg.appendChild(el('circle',{cx:n.x,cy:n.y,r:20,
      fill:c?COL.current:(v?COL.visited:COL.idle),
      stroke:c?COL.curStroke:(v?COL.visited:COL.idleStroke),'stroke-width':2}));
    const t=el('text',{x:n.x,y:n.y+5,'text-anchor':'middle',fill:COL.text,'font-size':14});
    t.textContent=(n.label!=null?n.label:n.id); svg.appendChild(t);
  });
}

// array (also stacks/queues via orient): {values:[], orient:'h'|'v', pointers:{name:idx}, highlight:Set}
function drawArray(a){
  clear(); const horiz=(a.orient||'h')==='h', bw=46,bh=40,gap=6,x0=40,y0=150;
  a.values.forEach((v,i)=>{
    const x=horiz?x0+i*(bw+gap):x0, y=horiz?y0:y0+i*(bh+gap);
    const hi=a.highlight&&a.highlight.has(i);
    svg.appendChild(el('rect',{x,y,width:bw,height:bh,rx:6,
      fill:hi?COL.current:COL.idle,stroke:hi?COL.curStroke:COL.idleStroke,'stroke-width':2}));
    const t=el('text',{x:x+bw/2,y:y+bh/2+5,'text-anchor':'middle',fill:COL.text,'font-size':14});t.textContent=v;svg.appendChild(t);
    const ix=el('text',{x:x+bw/2,y:y-8,'text-anchor':'middle',fill:'#888','font-size':11});ix.textContent=i;svg.appendChild(ix);
  });
  for(const name in (a.pointers||{})){const i=a.pointers[name];
    const x=horiz?x0+i*(bw+gap)+bw/2:x0-16, y=horiz?y0-26:y0+i*(bh+gap)+bh/2;
    const p=el('text',{x,y,'text-anchor':'middle',fill:COL.current,'font-size':12});p.textContent=name;svg.appendChild(p);}
}

// 2D grid for DP tables / matrices: {cells:[[..]], highlight:Set('r,c')}
function drawGrid(grid){
  clear(); const cw=46,ch=34,x0=60,y0=40;
  grid.cells.forEach((row,r)=>row.forEach((v,c)=>{
    const x=x0+c*cw, y=y0+r*ch, hi=grid.highlight&&grid.highlight.has(r+','+c);
    svg.appendChild(el('rect',{x,y,width:cw,height:ch,fill:hi?COL.current:COL.idle,stroke:'#555','stroke-width':1}));
    const t=el('text',{x:x+cw/2,y:y+ch/2+4,'text-anchor':'middle',fill:COL.text,'font-size':12});t.textContent=v;svg.appendChild(t);
  }));
}

// tree (also recursion trees): {root:{id,label,children:[]}, visited:Set, current:id}
function layoutTree(root){
  const nodes=[],edges=[]; let leaf=0; const dy=70,x0=50,y0=40;
  (function rec(n,depth){
    let mid; if(n.children&&n.children.length){const ks=n.children.map(c=>rec(c,depth+1));mid=(ks[0]+ks[ks.length-1])/2;}
    else mid=leaf++;
    nodes.push({id:n.id,x:x0+mid*64,y:y0+depth*dy,label:(n.label!=null?n.label:n.id)});
    (n.children||[]).forEach(c=>edges.push([n.id,c.id])); return mid;
  })(root,0);
  return {nodes,edges};
}
function drawTree(t){const {nodes,edges}=layoutTree(t.root);drawGraph({nodes,edges,visited:t.visited,current:t.current});}

// linked list: {values:[], pointer:idx}
function drawLinkedList(ll){
  clear(); const bw=54,bh=36,gap=34,x0=40,y0=150;
  ll.values.forEach((v,i)=>{
    const x=x0+i*(bw+gap), hi=ll.pointer===i;
    svg.appendChild(el('rect',{x,y:y0,width:bw,height:bh,rx:6,fill:hi?COL.current:COL.idle,stroke:hi?COL.curStroke:COL.idleStroke,'stroke-width':2}));
    const t=el('text',{x:x+bw/2,y:y0+bh/2+5,'text-anchor':'middle',fill:COL.text,'font-size':14});t.textContent=v;svg.appendChild(t);
    if(i<ll.values.length-1) svg.appendChild(el('line',{x1:x+bw,y1:y0+bh/2,x2:x+bw+gap,y2:y0+bh/2,stroke:COL.edge,'stroke-width':2}));
  });
}

/* ===== infrastructure: step engine + questions (do not edit) ===== */
const narration=document.getElementById('narration'),counter=document.getElementById('counter');
const quiz=document.getElementById('quiz'),qtext=document.getElementById('qtext'),qopts=document.getElementById('qopts'),reveal=document.getElementById('reveal');
const playBtn=document.getElementById('play'),speed=document.getElementById('speed');
let STEPS=[],idx=0,timer=null;
function render(){const s=STEPS[idx];s.draw();narration.textContent=s.note||'';counter.textContent=(idx+1)+' / '+STEPS.length;
  if(s.question)showQuestion(s.question);else quiz.hidden=true;}
function showQuestion(q){quiz.hidden=false;qtext.textContent=q.prompt;reveal.hidden=true;qopts.innerHTML='';
  q.options.forEach((o,i)=>{const b=document.createElement('button');b.textContent=o;
    b.onclick=()=>{reveal.hidden=false;reveal.textContent=(i===q.answer?'✓ Correct. ':'✗ Not quite. ')+q.explain;};qopts.appendChild(b);});}
function step(){if(idx<STEPS.length-1){idx++;render();}else pause();}
function prev(){if(idx>0){idx--;render();}}
function pause(){clearInterval(timer);timer=null;playBtn.textContent='▶ Play';}
function play(){if(timer){pause();return;}playBtn.textContent='⏸ Pause';timer=setInterval(()=>{if(idx>=STEPS.length-1){pause();return;}step();},+speed.value);}
function reset(){pause();idx=0;render();}
document.getElementById('prev').onclick=prev;
document.getElementById('step').onclick=()=>{pause();step();};
document.getElementById('reset').onclick=reset;
playBtn.onclick=play;

/* ===== EDIT BELOW: define the lesson ===== */
function buildSteps(){
  // EXAMPLE — BFS from node 0. Replace with the concept being taught.
  const N=[{id:0,x:320,y:50},{id:1,x:180,y:150},{id:2,x:460,y:150},
           {id:3,x:110,y:260},{id:4,x:250,y:260},{id:5,x:530,y:260}];
  const E=[[0,1],[0,2],[1,3],[1,4],[2,5]];
  const order=[0,1,2,3,4,5];
  const steps=[];
  for(let k=0;k<order.length;k++){
    const visited=new Set(order.slice(0,k));
    const cur=order[k];
    const node={nodes:N,edges:E,visited,current:cur};
    let question=null;
    if(k===1) question={prompt:"BFS just finished node 0. Which nodes are visited next?",
      options:["3 and 4 (go deep)","1 and 2 (the neighbors)","5 (the far node)"],answer:1,
      explain:"BFS uses a queue, so it visits all direct neighbors of 0 (nodes 1 and 2) before going deeper."};
    steps.push({draw:()=>drawGraph(node),note:"Visiting node "+cur+" — neighbors get queued.",question});
  }
  steps.push({draw:()=>drawGraph({nodes:N,edges:E,visited:new Set(order),current:null}),note:"All nodes visited. BFS complete."});
  return steps;
}
STEPS=buildSteps();render();
</script>
</body>
</html>
```

### Choosing a helper
| Concept shape | Helper |
|---|---|
| Graphs, state machines | `drawGraph` |
| Trees, recursion trees, heaps | `drawTree` (or `drawGraph` with explicit positions) |
| Arrays, two-pointers, sliding window, sorting | `drawArray` (use `pointers` and `highlight`) |
| Stacks, queues | `drawArray` with `orient:'v'` (stack) or `'h'` (queue) |
| DP tables, matrices, grids | `drawGrid` (use `highlight` with `"r,c"` keys) |
| Linked lists | `drawLinkedList` |

Keep each visual to ~6–14 steps. Put 1–2 questions at the moments a learner typically slips (pulled from their `past_mistakes` when relevant).

---

## Part B — Roadmap map generator

A roadmap is a clean prerequisite DAG for one area. Style rules (validated): centered foundations spine, **right-angle (orthogonal) connectors** (never diagonal), phase labels down the left gutter, **solid arrow = prerequisite / dashed = next phase**, the learner's current/next topic highlighted gold, and an "advanced/stretch" tier drawn dashed.

You supply: the area title, the `B` (boxes) map, the `L` (links) list, and the phase `labels`. Positions follow a tiered top-down grid; place each box so its children straddle it to keep connectors short and uncrossed. Status colors come from the progress file (`done`/`in-progress`/`not-started`).

Copy this whole file, replace `__AREA_TITLE__`, `B`, `L`, and `labels`:

```html
<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>__AREA_TITLE__ roadmap</title>
<style>body{margin:0;background:#15151f;color:#eee;font:15px/1.5 -apple-system,Segoe UI,Roboto,sans-serif}
.wrap{max-width:1140px;margin:0 auto;padding:20px}h1{font-size:20px}.legend{color:#bbb;font-size:13px}
svg{width:100%;height:auto}</style></head>
<body><div class="wrap">
<h1>__AREA_TITLE__ — learning roadmap</h1>
<p class="legend">Solid → prerequisite · Dashed ⇢ next phase · Gold = current/next · Dashed box = stretch</p>
<svg id="map" viewBox="0 0 1120 850"></svg>
</div>
<script>
const NS="http://www.w3.org/2000/svg",svg=document.getElementById('map'),W=200,H=54;
const C={found:'#3b82f6',current:'#e0b341',core:'#3fb950',app:'#14b8a6',struct:'#f59e0b',sp:'#a855f7',adv:'#9ca3af'};
// EDIT: boxes keyed by id -> {x,y,phase,label,sub}. phase 'current' highlights gold; 'adv' draws dashed.
const B={
  /* example (graphs); replace per area */
  term:{x:510,y:24,phase:'found',label:'Terminology',sub:'vertices · edges · paths'},
  adt:{x:510,y:106,phase:'current',label:'Graph ADT',sub:'the interface'},
  repr:{x:510,y:188,phase:'found',label:'Representations',sub:'adj list / matrix'}
};
// EDIT: links [from,to,type] where type 'p'=prerequisite(solid), 'n'=next-phase(dashed)
const L=[['term','adt','p'],['adt','repr','p']];
// EDIT: left-gutter phase labels [text, phaseColorKey, centerY]
const labels=[['FOUNDATIONS','found',110]];

const defs=document.createElementNS(NS,'defs');
defs.innerHTML='<marker id="as" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#8b8b9e"/></marker>'+
'<marker id="an" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#a7adc4"/></marker>';
svg.appendChild(defs);
function geo(n){return {cx:n.x+W/2,cy:n.y+H/2,top:n.y,bottom:n.y+H,left:n.x,right:n.x+W};}
function pathFor(s,t){const a=geo(s),b=geo(t);
  if(Math.abs(s.y-t.y)<1)return t.x>s.x?`M${a.right} ${a.cy} H${b.left}`:`M${a.left} ${a.cy} H${b.right}`;
  const my=(a.bottom+b.top)/2;return `M${a.cx} ${a.bottom} V${my} H${b.cx} V${b.top}`;}
L.forEach(([s,t,ty])=>{const p=document.createElementNS(NS,'path');p.setAttribute('d',pathFor(B[s],B[t]));
  p.setAttribute('fill','none');p.setAttribute('stroke',ty==='n'?'#a7adc4':'#8b8b9e');
  p.setAttribute('stroke-width',ty==='n'?'1.6':'2');if(ty==='n')p.setAttribute('stroke-dasharray','6,5');
  p.setAttribute('marker-end',ty==='n'?'url(#an)':'url(#as)');svg.appendChild(p);});
labels.forEach(([txt,ph,cy])=>{const t=document.createElementNS(NS,'text');t.setAttribute('x',26);t.setAttribute('y',cy);
  t.setAttribute('fill',C[ph]);t.setAttribute('font-size','11');t.setAttribute('font-weight','700');
  t.setAttribute('letter-spacing','1.5');t.setAttribute('text-anchor','middle');
  t.setAttribute('transform',`rotate(-90,26,${cy})`);t.textContent=txt;svg.appendChild(t);});
Object.values(B).forEach(n=>{const col=C[n.phase],cur=n.phase==='current',adv=n.phase==='adv';
  const r=document.createElementNS(NS,'rect');r.setAttribute('x',n.x);r.setAttribute('y',n.y);
  r.setAttribute('width',W);r.setAttribute('height',H);r.setAttribute('rx','9');
  r.setAttribute('fill',cur?'rgba(224,179,65,0.16)':'rgba(38,38,52,0.92)');
  r.setAttribute('stroke',col);r.setAttribute('stroke-width',cur?'3':'2');
  if(adv)r.setAttribute('stroke-dasharray','6,4');svg.appendChild(r);
  const t1=document.createElementNS(NS,'text');t1.setAttribute('x',n.x+14);t1.setAttribute('y',n.y+23);
  t1.setAttribute('fill','#fff');t1.setAttribute('font-size','14');t1.setAttribute('font-weight','700');t1.textContent=n.label;svg.appendChild(t1);
  const t2=document.createElementNS(NS,'text');t2.setAttribute('x',n.x+14);t2.setAttribute('y',n.y+41);
  t2.setAttribute('fill','#b8b8c8');t2.setAttribute('font-size','10.5');t2.textContent=n.sub;svg.appendChild(t2);});
</script>
</body>
</html>
```

When advancing a topic, regenerate the file with updated `phase`/status colors (mark completed topics `done`, set the new current topic to `phase:'current'`).
````

- [ ] **Step 3: Verify the file exists and is self-contained (the "passing test")**

Run:
```bash
f=/Users/kushalkrishnappa/Playground/dsa/.claude/skills/dsa-tutor/references/visual_authoring.md
ls "$f" && \
( grep -nE 'src="https?:|href="https?:|cdn|<link ' "$f" && echo "FAIL: external dependency found" || echo "OK: no external deps" ) && \
( grep -c "<!DOCTYPE html>" "$f" )
```
Expected: file lists; `OK: no external deps`; count `2` (concept template + roadmap template).

- [ ] **Step 4: Verify the concept template renders without JS errors**

Run:
```bash
python3 - <<'PY'
import re, pathlib
f="/Users/kushalkrishnappa/Playground/dsa/.claude/skills/dsa-tutor/references/visual_authoring.md"
html=re.search(r"```html\n(<!DOCTYPE.*?</html>)\n```", pathlib.Path(f).read_text(), re.S).group(1)
out=pathlib.Path("/private/tmp/claude-501/-Users-kushalkrishnappa-Playground-dsa/ff6d9757-ffbb-4aea-9022-4ba3d271faed/scratchpad/sample_visual.html")
out.write_text(html); print("wrote", out)
PY
node -e "process.exit(0)" 2>/dev/null && echo "node present (optional)" || echo "no node; open sample_visual.html in a browser to confirm it animates"
```
Expected: writes `sample_visual.html`. Open it in a browser to confirm the BFS animation plays, Step/Prev/Reset work, and the question reveals an answer.

---

## Task 3: Rewrite SKILL.md

**Files:**
- Modify (full rewrite): `.claude/skills/dsa-tutor/SKILL.md`

- [ ] **Step 1: Verify current broken/legacy state (the "failing test")**

Run:
```bash
grep -ni "download\|upload\|present.*for download" /Users/kushalkrishnappa/Playground/dsa/.claude/skills/dsa-tutor/SKILL.md
```
Expected: matches found (the legacy download/upload workflow) — these must be gone after the rewrite.

- [ ] **Step 2: Overwrite SKILL.md**

Overwrite `.claude/skills/dsa-tutor/SKILL.md` with exactly:

````markdown
---
name: dsa-tutor
description: A Socratic tutor for deep, durable understanding of any data structures & algorithms topic — arrays, linked lists, stacks, queues, hash tables, trees, heaps, graphs, sorting, searching, recursion, dynamic programming, greedy, two-pointers, sliding window, backtracking, Big-O, or any specific problem or pattern. Trigger for "teach me", "help me understand", "quiz me", "I keep forgetting", "test my memory", "explain X", "let's continue where we left off", "review", "interview prep". Progress is stored automatically on disk under .dsa-tutor/ and reloaded every session (an uploaded dsa_progress.json is imported once as a legacy fallback). The tutor builds mental models, gives mnemonics, asks one guiding question at a time, generates interactive visualizations, recommends practice problems, corrects mistakes with unforgettable examples, and tracks mastery via spaced repetition across days.
---

# DSA Tutor

You are a tutor whose single goal is **durable, transferable understanding** — the learner (intermediate level) should be able to *apply* concepts in interviews and *not forget* them. You achieve this through mental models, mnemonics, Socratic questioning, surgical error correction, generated interactive visualizations, and spaced repetition tracked in a progress file stored on disk.

This skill is **topic-agnostic**: it works for any DSA area. Nothing topic-specific is hard-coded — you generate roadmaps, visuals, and practice recommendations at runtime for whatever the learner is studying.

Never just dump information. Teaching here is a dialogue, not a lecture.

## Where everything lives (read this first, every session)

- **Project root** = the nearest ancestor directory containing a `.claude/` folder; if none, use the current working directory.
- **Progress file:** `<project-root>/.dsa-tutor/dsa_progress.json` — the learner's memory.
- **Roadmaps:** `<project-root>/.dsa-tutor/roadmaps/<area>.html`
- **Concept visuals:** `<project-root>/.dsa-tutor/visuals/<concept>.html`
- Create the directory/files with the Write tool as needed. **The learner never downloads or uploads anything.**

## At the very start of every session

1. **Read `.dsa-tutor/dsa_progress.json`** with the Read tool.
   - **Present** → run the **Returning-Learner Refresh** (below).
   - **Missing, but the user pasted/uploaded a `dsa_progress.json`** → write it to that path (one-time import), then refresh.
   - **Missing entirely** → this is a new learner — run **First-Session Setup**.
2. Do this *before* answering the substantive request. Even if the user jumps straight to "teach me heaps," a 3-line refresh first makes retention work.

### First-Session Setup
Briefly (2–3 sentences) explain how you'll work: one question at a time, mnemonics, interactive visuals you can open, you'll be corrected the instant you slip, and a progress file on disk tracks everything for spaced review. Ask what area they want to start with, or suggest one. Then begin the **per-topic cycle**, and write the progress file at the first checkpoint.

### Returning-Learner Refresh
Read `dsa_progress.json` and give a tight refresher (≤ ~8 lines):
- One line: what they last worked on and how it went.
- The **mnemonic(s)** for any topic they struggled with — repetition is the point.
- "Due for review today" — pull from the spaced-repetition schedule.
Then offer the **Daily Quick Quiz** before new material.

## The teaching method (apply to every concept)

### 1. Build the mental model first
Anchor the abstract concept to something physical, visual, or familiar before any formal definition. Examples of the style: Stack → a stack of plates (LIFO); Queue → a coffee-shop line (FIFO); Hash table → a coat-check (key → ticket → hook); Recursion → Russian nesting dolls; DP → a spreadsheet reusing computed neighbors. Then give the precise definition and the key invariant.

### 2. Give a mnemonic
Every concept gets a short, sticky memory hook, concrete and slightly absurd if that helps. Tailor it to what trips *this* learner up, and record it in the progress file so refreshers reuse it.

### 3. Teach for application, not recall
Immediately tie the concept to **when you'd reach for it**: state the tell-tale signal ("find a pair summing to target in a sorted array → two pointers"). This is what makes interview transfer happen.

### 4. Drive with questions, ONE at a time
After a short teach, ask a single guiding question and **stop**. Wait for the answer. Never stack questions. Progress from concrete to applied. Let them do the thinking.

### 5. When they're wrong — correct surgically + unforgettable example
- **Name the exact misconception** (not "not quite").
- **Give a dead-simple, memorable counterexample** that makes the error impossible to repeat.
- Re-ask a variant to confirm it stuck, and record the misconception in `past_mistakes`.

### 6. Coding fluency
After the concept clicks, have them implement or trace real code (their language; default Python) **in their own project files** — read and review that file; never relocate their code into `.dsa-tutor/`. Point out the one or two recurring idioms.

## The per-topic cycle

For each topic, run this loop and save progress after each checkpoint:
1. **Diagnose (adaptive)** — start with an easy question, adjust difficulty by their answers, and stop once their level is clear (usually 2–5 questions). One question at a time.
2. **Teach unforgettably** — apply the teaching method (mental model → mnemonic → definition → application trigger).
3. **Visualize** — generate `.dsa-tutor/visuals/<concept>.html` per `references/visual_authoring.md` (moving parts + 1–2 embedded "predict the next step" questions). Tell the learner to open it, then ask guiding questions tied to it, one at a time.
4. **Implement in Python** — they write/trace it in their own files; review and flag recurring idioms.
5. **Practice** — recommend problems (see **Practice problems**).
6. **Track & save** — update mastery, mnemonic, mistakes, aces, interval, and `practice_done`; write the file.
7. **Advance** — regenerate the area roadmap with updated statuses and pick the next available topic.

## Roadmaps (generate per area)

When the learner starts a new area, generate a roadmap map to `.dsa-tutor/roadmaps/<area>.html` following `references/visual_authoring.md` (orthogonal connectors, phase labels, solid = prerequisite / dashed = next phase, current topic gold, stretch tier dashed). Decompose the area into a prerequisite DAG from your own DSA knowledge. Record the roadmap path and the ordered topic list (with `status`) in the progress file's `curriculum` block. Regenerate it (updating statuses) when advancing.

## Practice problems

After a concept clicks, recommend 2–4 problems for that topic from your own knowledge, across **LeetCode**, **HackerRank**, and **dsapanicle.com**. Verify the dsapanicle.com link is reachable before giving it; if you can't confirm it, give the LeetCode/HackerRank problems and note that the dsapanicle.com link is unverified. Record what you recommended and what they solved in the concept's `practice_done`.

## Daily Quick Quiz (spaced repetition)
Offer this at the start of returning sessions, and any time the user asks to "test my memory" or "quiz me." Pull **3–5 short questions** from topics that are *due*, mixing recall, application, and one from a past mistake. Ask **one at a time**, grade each, and update the progress file. Keep it brisk.

## Spaced Repetition
Track a `review_interval` (days) per concept using a Leitner schedule:
- New / just-learned → review next session (interval 1).
- Answered correctly → roughly double (1 → 3 → 7 → 16 → 30).
- Answered wrong → reset to 1 and flag it.
A concept is "due" when `today - last_reviewed >= review_interval`. Surface due items first.

## Mastery tracking
Every graded answer updates the concept:
- **Correct** → advance `review_interval`, increment `aces`, raise `mastery` when warranted.
- **Wrong** → reset `review_interval` to 1, append the **exact misconception** to `past_mistakes`, lower `mastery`.
The Daily Quick Quiz preferentially re-pulls from `past_mistakes` + due items, reminding the relevant mnemonic each time — so you keep re-testing precisely what the learner tends to miss.

## Progress file (auto-persisted)
The file is the learner's memory across sessions. **Read it at session start; write it after every checkpoint (concept taught/updated, quiz graded, practice recorded) and at session end** using the Write tool to overwrite the whole file with updated content. Schema and an example live in `references/progress_schema.md` — read that file when creating or updating so the structure stays stable. Always set `last_session_date` to today and recompute intervals before writing. Keep the schema stable; only append/update entries.

## Tone
Warm, sharp, and economical. You're a coach who respects the learner's time and intelligence. Celebrate correct reasoning briefly; correct errors immediately and concretely. Default to prose and short dialogue turns — avoid walls of bullet points in the actual conversation. One question per turn, always.
````

- [ ] **Step 3: Verify download/upload language is gone and references resolve (the "passing test")**

Run:
```bash
d=/Users/kushalkrishnappa/Playground/dsa/.claude/skills/dsa-tutor
( grep -ni "download\|re-upload\|present.*for download" "$d/SKILL.md" && echo "FAIL: legacy language remains" || echo "OK: no download/upload language" )
for ref in progress_schema.md visual_authoring.md; do
  grep -q "references/$ref" "$d/SKILL.md" && ls "$d/references/$ref" >/dev/null && echo "OK: $ref referenced and exists" || echo "FAIL: $ref"
done
grep -q "preogress" "$d/SKILL.md" && echo "FAIL: misspelled ref remains" || echo "OK: no misspelled ref"
```
Expected: `OK: no download/upload language`; both refs `OK`; `OK: no misspelled ref`.

- [ ] **Step 4: Verify frontmatter is well-formed**

Run:
```bash
python3 - <<'PY'
import pathlib
t=pathlib.Path("/Users/kushalkrishnappa/Playground/dsa/.claude/skills/dsa-tutor/SKILL.md").read_text()
assert t.startswith("---\n"), "missing opening frontmatter fence"
fm=t.split("---\n",2)[1]
assert "name: dsa-tutor" in fm and "description:" in fm, "frontmatter missing name/description"
print("OK: frontmatter well-formed")
PY
```
Expected: `OK: frontmatter well-formed`.

---

## Task 4: End-to-end coherence verification

**Files:** none modified — this is a final checkpoint.

- [ ] **Step 1: Verify the whole skill package is coherent**

Run:
```bash
d=/Users/kushalkrishnappa/Playground/dsa/.claude/skills/dsa-tutor
echo "== files ==" && ls -1 "$d" "$d/references"
echo "== no misspelled file ==" && ( ls "$d/references/preogress_schema.md" 2>/dev/null && echo FAIL || echo OK )
echo "== schema JSON parses ==" && python3 - <<'PY'
import re,json,pathlib
b=re.search(r"```json\n(.*?)\n```",pathlib.Path("/Users/kushalkrishnappa/Playground/dsa/.claude/skills/dsa-tutor/references/progress_schema.md").read_text(),re.S).group(1)
json.loads(b);print("OK")
PY
echo "== visuals self-contained ==" && ( grep -nE 'src="https?:|href="https?:' "$d/references/visual_authoring.md" && echo FAIL || echo OK )
```
Expected: both reference files present (`progress_schema.md`, `visual_authoring.md`), no `preogress_schema.md`, schema JSON `OK`, self-contained `OK`.

- [ ] **Step 2: Manual smoke test of the live skill**

In a new conversation (or by invoking the skill), say "teach me graphs". Confirm the tutor:
- Reads/creates `.dsa-tutor/dsa_progress.json` (no download/upload prompt).
- Runs a short adaptive diagnostic, one question at a time.
- Generates `.dsa-tutor/roadmaps/graphs.html` and at least one `.dsa-tutor/visuals/*.html`, and points you to open them.
- Writes progress to disk after the first checkpoint.

Expected: all four behaviors observed; `.dsa-tutor/` is populated on disk.

---

## Self-Review

**Spec coverage:**
- Auto-persist under `.dsa-tutor/` → Task 3 (lifecycle, project-root resolution, write-after-checkpoint) + Task 1 (schema location). ✓
- Continuous + end-of-session saves → Task 3 (per-topic cycle step 6, Progress file section). ✓
- Generic / no topic-specific content → Tasks 2 & 3 (templates + runtime generation; example code clearly marked "replace"). ✓
- Interactive visuals with moving parts + embedded questions → Task 2 Part A. ✓
- Generated per-area roadmap (validated style) → Task 2 Part B + Task 3 Roadmaps section. ✓
- Adaptive diagnostic → Task 3 per-topic cycle step 1. ✓
- Implement in own files → Task 3 teaching method §6 + cycle step 4. ✓
- Practice recommendations (LeetCode/HackerRank/dsapanicle.com), recorded → Task 3 Practice section + Task 1 `practice_done`. ✓
- Mastery tracking (aces/mistakes, re-drill) → Task 3 Mastery section + Task 1 `aces`/`past_mistakes`. ✓
- Cleanups (rename, remove download language, verify dsapanicle.com) → Task 1, Task 3, Task 3 Practice. ✓

**Placeholder scan:** Example code blocks are explicitly labeled "EXAMPLE … replace" — these are illustrative templates, not unfinished work. No "TBD"/"TODO"/"implement later". ✓

**Type/name consistency:** Field names (`curriculum`, `topics`, `current`, `aces`, `visual`, `practice_done`, `review_interval`, `past_mistakes`) match across Task 1 schema and Task 3 usage. Helper names (`drawGraph`, `drawArray`, `drawGrid`, `drawTree`, `layoutTree`, `drawLinkedList`) are defined and referenced consistently in Task 2. Paths `.dsa-tutor/{roadmaps,visuals}/` consistent across tasks. ✓
