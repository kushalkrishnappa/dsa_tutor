# Visual Authoring Guide

How to generate the two visual artifacts the tutor uses. Both are **self-contained HTML** — inline CSS/JS, no external `src`/`href`, no CDNs — written with the Write tool so they work offline and persist for the learner to revisit.

- **Concept visuals** → `<topic-folder>/.dsa-tutor/visuals/<concept>.html` (slug the concept name, e.g. `breadth-first-search` → `bfs.html`).
- **Roadmap maps** → `<topic-folder>/.dsa-tutor/roadmap.html`.

`<topic-folder>` is the active folder for the session — each DSA topic keeps its own visuals beside its own code. Paths recorded in `progress.json` are relative to that folder (`.dsa-tutor/visuals/bfs.html`).

Create the directory on first write. Tell the learner to open the file (e.g. `file://<absolute-path>` or via the IDE).

**These are dual-coding aids, not handouts.** A visual works when you narrate *while* the learner has it open, pointing at what's on screen. One generated at the end of a lecture and handed over unexplained does nothing.

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
