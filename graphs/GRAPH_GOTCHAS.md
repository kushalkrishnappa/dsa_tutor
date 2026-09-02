# Graphs — The Field Guide: Every Concept, Every Trap

A field guide to graphs, written from working through them one concept at a time. Same spirit as
`trees/BINARY_TREE_GOTCHAS.md`: each section is a trap, why it happens, and the fix — with runnable
Python. The traps here are the ones *I actually hit*, so this doubles as a map of my own soft
spots. Read it before an interview; re-read the ones marked ⚠️ **recurring**.

Concepts covered, in the order I learnt them: terminology → representations → BFS → DFS → the
traversal framework → connected components → cycle detection → topological sort → union-find.

---

## 1. A graph is just "nodes + relationships" — and `visited` is the seatbelt

**Mental model:** Google Maps. Intersections = vertices, roads = edges. One-way streets =
**directed** edges, distances = **weights**. That's the whole vocabulary.

The one non-negotiable habit: **mark before you walk.** A `visited` set is the seatbelt that stops
a cycle from looping you forever. Trees don't need it (no cycles, exactly one path between nodes);
general graphs *always* do.

Two number traps carried over from trees, worth restating in graph language:

- **Degree ≠ child count.** A node's *degree* is how many edges touch it. In an undirected graph a
  node in the middle of a path has degree 2 even though it's nobody's "child."
- **Connected ≠ tree.** A tree is connected **and** acyclic — equivalently, connected with exactly
  `N−1` edges. One extra edge guarantees a cycle. `len(edges) == n - 1` is an O(1) tree check.

---

## 2. Adjacency list vs matrix: know the *currency* ⚠️ recurring

**Mental model:** the adjacency **list** is your phone contacts — only the people you actually
know. The adjacency **matrix** is a `V × V` seating grid with a cell reserved for *every possible
pair*, whether they know each other or not.

> **List = Lean (sparse). Matrix = Massive (dense).**

The trap I kept falling into was **pricing operations in the wrong currency**:

| Operation | Adjacency list | Adjacency matrix |
|---|---|---|
| Space | `O(V + E)` | `O(V²)` **always** |
| Is `u`–`v` an edge? | `O(degree(u))` | `O(1)` ← matrix's one superpower |
| Iterate `u`'s neighbours | `O(degree(u))` | `O(V)` (scan the whole row) |

Two ways I got this wrong, both logged:

- **Sizing the matrix by edge count.** A matrix is `V²` *regardless of edges*. 10M nodes with zero
  edges is still 100 trillion cells. Edges never shrink it.
- **Pricing list ops in `V`.** I once said iterating a list node's neighbours costs `O(V)`. It
  doesn't — the list's currency is **degree**. In a `V=100k`, `E=200k` graph the average degree is
  ~4, so it's `O(4)`, not `O(100000)`. The list *exists* precisely to dodge the matrix's row-scan.

> **The currency: List = pay per FRIEND (degree). Matrix = pay per SEAT in the row (V).**
> Degree can coincidentally equal `V−1` (a celebrity node everyone knows) — that doesn't make the
> pricing rule wrong, it's just the one case where the two currencies collide.

My real builder (`graphs.py`), undirected, with isolated nodes pre-initialised:

```python
from collections import defaultdict

def build_adjacency_list(num_nodes, edges):
    adj = defaultdict(list)
    for i in range(num_nodes):
        adj[i] = []                 # pre-init so isolated nodes still appear
    for start, end in edges:
        adj[start].append(end)
        adj[end].append(start)      # both directions -> undirected
    return adj
```

**Sub-trap: dict keys `1` and `'1'` are different keys.** I once pre-initialised isolated nodes
with `str(i)` keys while the edges used `int` labels, so `adj[1]` and `adj['1']` silently became
two separate entries (`1 == '1'` is `False`). If half your graph vanishes, check that your node
labels are all the *same type*.

---

## 3. Extracting matrix neighbours: the index-vs-value trap ⚠️⚠️ recurring (hit 4×)

This is my most persistent bug. When neighbours come from an adjacency **matrix** row, the
neighbours are the **column indices where the cell is 1** — *not* the row values themselves.

**The physical anchor that finally stuck** (after talking it through failed three times): a matrix
row is a **street of houses**. The number inside a house (`0`/`1`) is only its **porch light**
(on/off). A neighbour is a **house number** — an address — never a light state.

```python
row = [1, 0, 1, 1, 0]   # street: house 0 light ON, house 1 OFF, house 2 ON, ...

# WRONG — walks the street seeing only lights, loses track of where it's standing:
[nb for nb in row if row[nb] == 1]        # nb takes VALUES 1,0,1,1,0 -> indexes garbage -> [0, 0]

# RIGHT — read the house NUMBER off the mailbox with enumerate:
i = 2
[j for j, val in enumerate(row) if val == 1 and j != i]   # -> [0, 3]  (j != i drops the self-loop)
```

Two slots, two jobs — mixing them is the whole bug:

> **The NUMBER is the ANSWER. The LIGHT is the TEST.** `enumerate` hands you both, one per job:
> `for j, val in enumerate(row)` → `j` is the address you *emit*, `val` is the light you *filter on*.

Three disguises this bug wore, so I recognise it next time:

1. `for nb in row` yields **values**, not indices. `enumerate(row)` yields `(index, value)` —
   **INDEX FIRST** (mnemonic: e-**NUM**-erate, the NUMber comes first, like "1. eggs").
2. Comprehension slot order is `[WHAT for VAR in WHERE if CONDITION]` — the output expression
   comes first (it's the `append()` yanked to the front).
3. The self-loop lives on the **diagonal** `M[i][i]` — exclude with `and j != i`, not some other
   index. (And it's `j != i`, not `val != 2` — a `0/1` light can *never* equal `2`, so that filter
   does nothing.)

> **The smell detector:** in a 5-node graph, legal indices are `0..4`. If the thing you're
> indexing/comparing with can only ever be `0` or `1`, **you're using a light switch as an
> address.** That single check catches all four disguises.

General form, memorise it cold: `[j for j, val in enumerate(M[i]) if val == 1 and j != i]`.

---

## 4. One engine, two knobs — BFS/DFS never change ⚠️ the unifying idea

The single most transferable graph insight. **BFS and DFS never change.** Across
tree / graph / grid / matrix, only **two knobs** turn:

1. **the neighbour function** — how you find who's adjacent
2. **whether you need `visited`** — and how you represent it

| Structure | Neighbours | Visited? |
|---|---|---|
| Tree | `node.left, node.right` | not needed (acyclic) |
| Graph | `adj[node]` | `set()` |
| Grid | 4 directions + bounds check | mark cell in place |
| Matrix | `j where M[i][j] == 1` (§3!) | `set()` |

> **Same engine, two knobs: NEIGHBORS + VISITED.**
> Shortest / levels → **BFS**. Explore-all / paths / components / cycles → **DFS.**

A grid is just an *implicit* graph — you never build an adjacency list, you compute neighbours on
the fly from `(r±1, c)` and `(r, c±1)` with a bounds check. Recognising "grid = implicit graph" is
what lets you reuse the exact same DFS/BFS you already wrote.

---

## 5. BFS trap #1: mark visited on ENQUEUE, not dequeue ⚠️ recurring

```python
from collections import deque

def bfs(graph, start):
    order, q = [], deque([start])
    visited = {start}                 # marked at enqueue time
    while q:
        node = q.popleft()
        for nb in graph[node]:
            if nb not in visited:
                visited.add(nb)       # <-- mark HERE, the instant it enters the queue
                q.append(nb)
        order.append(node)
    return order
```

If you mark visited on **dequeue** instead, the same node can be enqueued *multiple times before
it's ever processed*. Diamond graph `A–B, A–C, B–D, C–D`: `B` and `C` both enqueue `D` before `D`
is dequeued, so `D` lands in the queue twice. It still terminates (a skip-guard on dequeue saves
correctness) but it floods the queue with duplicates. **Mark-on-enqueue makes each node enter the
queue exactly once.**

---

## 6. BFS trap #2: *why* first-arrival is the shortest path ⚠️ was a real depth-gap

It is not enough to say "FIFO" — that just restates what a queue is. And "the first time we reach
the target it must be shortest" is **circular** (it assumes the very thing to prove). The real
reason is the **monotone-queue invariant**:

> At any moment the BFS queue holds nodes from **at most two rings**: distance `d` and distance
> `d+1`, in that order. A ring-`(d+1)` node is only ever let into line *by* a ring-`d` node, so
> nothing farther away can jump the line.

Concretely, snapshot the queue's distances as you pop on `A–B, A–C, B–D, C–D, D–E`:

| pop | distances in queue |
|---|---|
| A(0) | {1, 1} |
| B(1) | {1, 2} |
| C(1) | {2} |
| D(2) | {3} |

`E(3)` can't *enter* the queue until `D(2)` is dequeued; for a 4 to sit in the queue a 3 must
already be out; for a 3 to be out all 2s must be gone. So a node's **first** arrival is along a
shortest path, and BFS can stop the instant it pops the target.

> **FIFO keeps the wave SORTED** — the queue never goes backwards in distance. That's why "nearest
> / fewest-steps / shortest unweighted" → reach for BFS, and DFS can't do it (no early exit; a
> shallower answer could be hiding down any branch).

*(Weighted edges break this — equal-hop no longer means equal-cost. That's what Dijkstra is for,
still ahead on my roadmap.)*

---

## 7. DFS trap: mark BEFORE you recurse ⚠️ recurring

```python
def dfs_recursive(graph, start):
    order, visited = [start], {start}
    def dfs(node):
        for nb in graph[node]:
            if nb not in visited:
                visited.add(nb)       # mark BEFORE the recursive call
                order.append(nb)
                dfs(nb)
    dfs(start)
    return order
```

Mark **after** the recursive call and you get infinite recursion. I proved this live on LeetCode
733 (Flood Fill): writing `dfs(nr, nc)` *then* `grid[nr][nc] = new` means the neighbour is never
marked before you dive into it, so the two cells keep re-inviting each other — `RecursionError` on
input as small as `[[1,1,1]]`. **Mark before recurse** is the recursive twin of *mark-on-push*.

Two more DFS facts worth keeping:

- **No `global`/`nonlocal` needed here.** The nested `dfs` only *mutates* `order`/`visited`
  (`append`/`add`), never rebinds them, so the closure shares them for free. `global` would just
  leak module names — a smell. (Contrast §11's `dia`, which *is* reassigned and so needs
  `nonlocal`.)
- **Recursive DFS dies past Python's ~1000-frame limit.** A 2000-node chain (e.g. LC 207 with a
  long prerequisite chain) blows the stack. Iterative DFS doesn't.

---

## 8. Iterative DFS: push vs pop, and the LIFO flip

Recursion is just a stack you can hold yourself. Two *valid* marking strategies — don't mix them:

```python
def dfs_iterative(graph, start):
    order, stack, visited = [], [start], {start}
    while stack:
        node = stack.pop()
        for nb in graph[node]:
            if nb not in visited:
                visited.add(nb)       # mark-on-PUSH: each node enters the stack once, no dups
                stack.append(nb)
        order.append(node)
    return order
```

- **Mark-on-push** (above): mark the instant you push. No duplicates ever sit on the stack.
- **Mark-on-pop + skip-guard**: push freely, mark when you pop, and `if node in visited: continue`
  at the top. This mirrors recursion and *allows* duplicates on the stack — the guard dedupes them
  when they re-pop. My grid flood-fill used this (`if grid[r][c] == 0` is the dedupe guard).

> The bug to avoid: mark-on-push but *also* keep a pop-guard like `if grid[r][c] == 1` — that's a
> contradiction (you already marked it, so the guard is either dead code or fatally wrong).

**The LIFO flip:** an explicit-stack DFS dives into the **last-listed** neighbour first (opposite
of recursion, which takes the first). Push `reversed(neighbours)` if you need to mirror recursive
order exactly. (Same rule as trees: *push in the reverse of the order you want to pop*.)

---

## 9. Connected components: the outer loop finds dry land

**Mental model:** islands in an ocean. Each maximal group of mutually-reachable nodes is one
island. You need **two** loops — and confusing their jobs is the classic bug:

```python
def count_components(graph):
    visited, count = set(), 0
    for node in graph:                     # OUTER: find fresh dry land
        if node not in visited:
            count += 1                     # a brand-new island
            dfs(node, graph, visited)      # INNER: flood this entire island
    return count
```

> **Outer loop = find dry land; inner traversal = flood the whole island. `count += 1` per fresh
> island.**

The outer-loop guard (`if node not in visited`) is the same guard connected components, cycle
detection, and topological sort all share — it's what makes them work on **disconnected** graphs.
Drop it and you either re-flood islands you've already counted, or (in cycle detection) call DFS on
a finished node and get a false positive.

---

## 10. Cycle detection: `visited` has TWO jobs, and one axis can't do both ⚠️ the core idea

The deepest confusion I untangled. A plain 2-state `visited` set does exactly **one** thing:
guarantees **termination** by refusing to re-recurse. It **cannot** tell you *why* a node was
re-seen:

- re-seen because it's **still on my current path** → that's a **cycle**
- re-seen because it's **already finished** → harmless **convergence**, not a cycle

Those need a **second axis of information**. Plain `visited` doesn't have it.

> **Plain `visited` STOPS loops (termination); the second axis DETECTS them (a cycle).**

### The unifying fact: a cycle *is* a back edge, nothing else

Classify every DFS edge by the colour of the node it lands on:

| Neighbour colour | Meaning | Edge type | Cycle? |
|---|---|---|---|
| WHITE (unseen) | recurse into it | tree edge | no |
| GRAY (on the current DFS stack) | points back to an ancestor | **back edge** | **YES** |
| BLACK (fully finished) | converged onto a done subtree | forward/cross edge | no |

A cycle exists **iff** DFS finds an edge to a GRAY node. That one rule covers *both* directed and
undirected graphs — they only differ in *which colours can occur*.

---

## 11. Cycle detection: directed vs undirected — STACK vs DOOR ⚠️ recurring

**Directed = one-way streets. Undirected = two-way streets.** This is why the two algorithms look
different.

**Directed** — watch the **STACK**. You need 3 colours, because an edge to a BLACK (finished) node
is *not* a cycle (it's convergence), so you must distinguish GRAY from BLACK. And you must **not**
skip the parent — `A→B` plus `B→A` are two distinct edges = a real 2-cycle.

```python
from collections import defaultdict

def has_cycle_directed(graph):
    WHITE, GRAY, BLACK = 0, 1, 2
    status = defaultdict(int)                     # default WHITE
    def dfs(node):
        status[node] = GRAY                       # on the stove
        for nb in graph[node]:
            if status[nb] == GRAY: return True    # back edge -> cycle
            if status[nb] == WHITE and dfs(nb): return True
        status[node] = BLACK                      # served & safe (the UN-graying)
        return False
    return any(status[n] == WHITE and dfs(n) for n in graph)
```

**Undirected** — watch the **DOOR** (where you came from). A plain `visited` set suffices: there
are **no cross/forward edges** in undirected DFS, so *any* visited non-parent neighbour is
guaranteed to be a GRAY ancestor. Just skip the parent.

```python
def has_cycle_undirected(graph):
    visited = set()
    def dfs(node, parent):
        if node in visited: return True           # check-on-entry (mark-on-pop twin)
        visited.add(node)
        for nb in graph[node]:
            if nb != parent and dfs(nb, node): return True
        return False
    return any(n not in visited and dfs(n, -1) for n in graph)
```

The mnemonic that fixed my repeated inversion of the 2-cycle question:

> **U-TURN vs ROUNDABOUT.** Walking one *undirected* edge back the way you came is a **U-turn** —
> one edge, innocent — and that's *exactly* what parent-skip skips. Two *directed* edges `A→B`,
> `B→A` are a **roundabout** — two distinct edges, a real 2-cycle — which is *exactly* why directed
> must **not** skip the parent. The definition underneath: a cycle exists when a node on the path
> is reached from an **entirely separate edge.**

> **Gray for one-way, Parent for two-way.** Parent-skip is a *feature* in undirected and would be a
> *bug* in directed.

### Sub-trap: `BLACK`/`DONE` is used *negatively*

In `has_cycle_directed`, no `if` ever tests for `BLACK`. So what's it for? Setting a node BLACK is
the **un-graying** — it takes the node *off* the stove so it stops testing positive for GRAY.
Delete `status[node] = BLACK` and a plain DAG (e.g. a diamond) false-positives, because the
converged node is still wrongly GRAY. You never test for black; **black is how a node stops testing
as gray.**

---

## 12. Topological sort: a LINEUP, not a WALK ⚠️ the key misconception

**Mental model:** getting dressed. Socks before shoes, pants before belt. The topological order is
the single sequence you put *every* garment on — and unrelated garments (socks vs shirt) both still
appear.

The misconception I hit head-on: **a topological order is not a path.** Consecutive nodes need
**not** be adjacent.

> Lay every node on a line left-to-right. The order is valid **iff every edge points RIGHT.**

For `A→C, B→C, C→D`: `A, B, C, D` is valid *even though `A→B` is not an edge*. Two disconnected
nodes `X, Y` have a valid topo order (`X,Y` or `Y,X`) yet no path between them at all. A *path*
requires adjacency between consecutive nodes; a *lineup* does not.

**Kahn's algorithm** — in-degree = your **WAIT COUNT** (how many nodes you're still waiting on);
`0` = free to walk. Placing a node lets everyone waiting on it cross a name off; a node joins the
ready pool only when its **last** blocker leaves:

```python
from collections import deque

def topological_sort(graph):
    indeg = {u: 0 for u in graph}
    for u in graph:
        for v in graph[u]:
            indeg[v] += 1
    pool = deque(u for u in graph if indeg[u] == 0)   # everyone free at the start
    order = []
    while pool:
        u = pool.popleft()
        order.append(u)
        for v in graph[u]:
            indeg[v] -= 1                              # cross u off v's wait list
            if indeg[v] == 0:                          # v's LAST blocker just left
                pool.append(v)
    return order if len(order) == len(graph) else None   # see §13
```

> The pool can be a queue, a stack, a heap — the container only picks **which** valid order you
> get, never **whether** it's valid.

---

## 13. Topological sort: SHORT LINEUP = CYCLE ⚠️ was a detection-rule gap

The tempting-but-wrong cycle test is "the pool started empty → cycle." That only catches graphs
with *no* free node at all. It misses graphs where the pool starts non-empty and only **empties
partway**.

Trace `A→B, B→C, C→B`: the pool starts as `[A]` (non-empty!), you place `A`, then `B` and `C` are
stuck waiting on each other forever. The pool drains with `B, C` never placed.

> **Count the LINEUP, not the pool.** If `len(order) < n` when the pool runs dry, the leftovers are
> all waiting on each other = deadlock = cycle.

That single integer comparison (`len(order) == len(graph)`) gives you **LC 207 Course Schedule**
for free — it's the same cycle detection as §11, wearing a scheduling story.

---

## 14. Union-Find: GROUPS and LEADERS, and the loser pays ⚠️ recurring bugs

**Mental model (my own vocabulary — GROUPS and LEADERS):** each member stores only their immediate
**boss** (a parent pointer). The **leader** is whoever is their own boss. `find` = climb the boss
chain to the leader; `union` = the losing leader gets a new boss.

Why not just store everyone's leader directly? Because then a merge must **relabel the entire
losing group** — O(size). The boss-pointer scheme makes union O(1): only the losing *leader's*
record changes.

```python
class UnionFind:
    def __init__(self):
        self.leader = {}
        self.size = {}

    def find(self, node):
        if node != self.leader.setdefault(node, node):   # lazy: register on first sight
            self.leader[node] = self.find(self.leader[node])  # path compression
        return self.leader[node]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                     # already same group -> redundant edge / cycle
        sa = self.size.setdefault(ra, 1)
        sb = self.size.setdefault(rb, 1)
        if sa < sb:                          # small joins large
            ra, rb = rb, ra
        self.leader[rb] = ra                 # loser's LEADER points at winner's leader
        self.size[ra] += self.size[rb]       # absorb the WHOLE roster
        return True
```

Three bugs I actually hit, each with the anchor that killed it:

- **`size[winner] += 1` instead of `+= size[loser]`.** ⚠️ *Insidious* — it's accidentally correct
  whenever the loser is a **singleton**, so it hides until you merge a group with real members.
  On a stream where the loser has 2 members, `+= 1` prints one too few. Anchor: *the merger
  acquired the company but only put the CEO on payroll — absorb the whole ROSTER.*
- **Path-compression rebinding no-op.** Writing `node = self.find(self.leader[node])` rebinds the
  *local name* to the root, then `self.leader[node] = node` stamps the **root's** own record
  (a no-op). Compression silently vanishes while every test still passes (find is still correct).
  Anchor: *you gave the CEO the CEO's speed-dial — the member who called never got the number.*
  Fix: each frame must write the returned root into **its own** node's entry while `node` still
  means the caller (the one-liner above does this).
- **Union links the ENDPOINTS, not the leaders.** `union(a, b)` must point `find(b)`'s leader at
  `find(a)`'s leader — never `b` at `a` directly. Linking the raw endpoints corrupts the forest.

Why the optimisations matter:

> Lazy unions build a **CONGA LINE** (the skewed-BST disease — `find` degrades to O(n)).
> **Fix 1, small-joins-large:** depth only grows when you *lose*, and losing at least doubles your
> group, so height ≤ log₂n. **Fix 2, path compression:** climb once, and everyone you passed gets
> the leader's **speed-dial**. Together ≈ O(1) amortised (inverse Ackermann ≤ 5).

---

## 15. Counting components with Union-Find: count the retired leaders ⚠️ a real miss

The idiom I got wrong: I tried a `find`-only comprehension with **no `union` call**. `find` without
`union` is **diagnosis without treatment** — nothing ever merges, so the count is meaningless.

The fix uses `union`'s **boolean return value** as the counter. Start with `n` one-person groups;
every `union` that returns `True` fuses two groups into one, **retiring exactly one leader**; a
`False` (endpoints already share a group) retires nobody.

```python
def count_components(n, edges):
    uf = UnionFind()
    return n - sum(uf.union(u, v) for u, v in edges)   # True sums as 1
```

> **Count the retired leaders.** `components = n − (number of successful unions)`. Exact because
> every merge takes two groups in and puts one out — never two, never zero.

And a `False` return is itself useful: it means the edge is **redundant** — both endpoints were
already connected, so this edge **closes a cycle**. That's the entire answer to **LC 684 Redundant
Connection**: the edge whose `union` returns `False`.

---

## Summary table

| # | Trap | One-line fix |
|---|---|---|
| 1 | Forgetting cycles loop forever | `visited` is the seatbelt — mark before you walk |
| 2 | Pricing ops in the wrong currency | List = pay per FRIEND (degree); Matrix = pay per SEAT (V), always V² |
| 2 | `1` vs `'1'` as dict keys | Keep all node labels the same type |
| 3 | Matrix neighbours = row values | Neighbours are indices where cell==1: `[j for j,v in enumerate(M[i]) if v==1 and j!=i]` |
| 4 | Rewriting BFS/DFS per structure | One engine, two knobs: NEIGHBORS + VISITED |
| 5 | BFS enqueues a node twice | Mark visited on **enqueue**, not dequeue |
| 6 | "First arrival is shortest" (circular) | Monotone-queue invariant: queue holds only rings d and d+1 |
| 7 | Infinite recursion in DFS | Mark **before** you recurse |
| 8 | Iterative DFS stack duplicates | Pick one: mark-on-push (no dups) *or* mark-on-pop + skip-guard |
| 9 | Missing islands in a disconnected graph | Outer loop finds dry land; inner floods; guard `if node not in visited` |
| 10 | Plain `visited` "detects" cycles | It only ensures termination — a cycle needs the 2nd (on-stack) axis |
| 11 | Same rule for directed & undirected | STACK vs DOOR: 3 colours + no parent-skip (directed) vs visited + parent-skip (undirected) |
| 11 | Deleting the BLACK assignment | BLACK is used negatively — it's the un-graying; delete it → false positive on DAGs |
| 12 | Topo order treated as a path | It's a LINEUP not a WALK — every arrow points right; consecutive nodes needn't be adjacent |
| 13 | "Empty pool at start = cycle" | Count the lineup: `len(order) < n` when pool drains = cycle |
| 14 | `size += 1` on union | Absorb the whole ROSTER: `size[winner] += size[loser]` |
| 14 | Path-compression rebinding no-op | Write the root into the caller's own dict entry, not the root's |
| 15 | `find`-only component count | Count retired leaders: `n − sum(union(u,v) for ...)` |
