# Binary Tree Recursion — Gotchas Nobody Tells You Upfront

A field guide to the traps in binary tree recursion, written from working through them one by
one. Each section is a trap, why it happens, and the fix — with runnable Python.

## 1. A tree is "connected + acyclic," not just "connected"

It's tempting to define a tree as "a connected graph." That's necessary but not sufficient — you
also need **acyclic**. The precise, load-bearing version is an edge count:

> To connect N nodes you need **at least** N−1 edges. N−1 edges, connected, leaves **zero slack**.
> One more edge than that and you are *guaranteed* a cycle — not "might have one," guaranteed.

Try to draw 3 connected nodes with 3 edges. You can't avoid a triangle — there's nowhere else for
the third edge to go. This gives three equivalent definitions of a tree, pick whichever is
cheapest for the problem: (1) connected + acyclic, (2) connected + exactly N−1 edges, (3) exactly
one path between every pair of nodes. Definition 2 is the one that wins interviews — it's an O(1)
check on the input (`len(edges) == n - 1`).

**Related trap:** a binary tree node has at most 2 *children*, but a non-root internal node has
**3 neighbours** in graph terms (parent + 2 children). Child-count and graph-degree are not the
same number — don't conflate them when a problem talks about "adjacent nodes."

## 2. The recursion contract: two blanks, and how to fill them

Every bottom-up tree function is the same skeleton:

```python
def solve(node):
    if node is None:
        return IDENTITY          # what does "nothing" contribute to the answer?
    left  = solve(node.left)     # TRUST this. Do not trace into it.
    right = solve(node.right)    # TRUST this too.
    return COMBINE(left, right, node.val)
```

The skill is not tracing the whole call tree in your head — it's **trusting the recursive call**
and only reasoning about what *this one node* does with two already-correct answers. Two blanks,
two questions:

- **COMBINE** — how do I fold my children's answers together with my own value?
- **IDENTITY** — what does an *empty* subtree contribute?

Two ways to find IDENTITY:
- **Direct:** ask "what does nothing contribute?" — obvious for sums (`0`) and counts (`0`).
- **Backsolve from the leaf:** figure out what a *leaf* must correctly return, then work out what
  `None` has to return to make the leaf's formula produce that. This is how you get `height()`'s
  famous `-1` base case: a leaf must have height `0`, and `1 + max(x, x) == 0` forces `x == -1`.

```python
def count_nodes(node):          # IDENTITY = 0, COMBINE = left + right + 1
    if node is None: return 0
    return count_nodes(node.left) + count_nodes(node.right) + 1

def height(node):                # IDENTITY = -1, COMBINE = 1 + max(left, right)
    if node is None: return -1
    return 1 + max(height(node.left), height(node.right))
```

`count_nodes` and `sum_values` and `height` differ by *one token* in COMBINE. That's the whole
point of the contract — you're not learning N algorithms, you're learning one skeleton and two
questions.

## 3. `if not node` vs `if node is None` — a real bug, not a style nit

These look interchangeable and usually are — until `TreeNode` gets a `__bool__` or `__len__`
(common if a node ever reports its own subtree size, or holds a value like `0` that some code
naively treats as "empty"):

```python
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right
    def __bool__(self):
        return self.val != 0        # innocuous-looking, common in real code

def count_nodes(node):
    if not node:              # BUG: calls __bool__, not an emptiness check
        return 0
    return count_nodes(node.left) + count_nodes(node.right) + 1
```

Python's truth-test protocol: `__bool__` is checked first and wins outright; `__len__` is only
consulted as a fallback when `__bool__` doesn't exist. Either one can make a *real* node falsy.

Walk a tree containing a node with value `0` through `count_nodes` above: `not node` calls
`__bool__`, gets `False` (falsy), and the function returns `0` **immediately** — without
recursing into that node's children. It's not just that one node is miscounted: **the entire
subtree beneath it is silently dropped.** A truthiness check on a node doesn't misjudge the node,
it amputates its descendants.

**Fix:** always use `is None` for tree-node absence checks. It asks "is anyone home?" — a question
no dunder method can spoof.

```python
if node is None:   # correct: asks about identity, immune to __bool__/__len__
```

## 4. Preorder / inorder / postorder are one walk, not three algorithms

```python
def dfs(node):
    if node is None: return
    # visit here -> PREORDER   (root, then children)
    dfs(node.left)
    # visit here -> INORDER    (left, root, right)
    dfs(node.right)
    # visit here -> POSTORDER  (children, then root)
```

Slide the "visit" line to one of three slots in a node's frame and you get a different order from
*the exact same traversal*. The tell for which one to use:

- **Postorder** = the recursion contract's order. Use it whenever a node's answer **depends on
  its children's answers** (height, diameter, node counts, "is this subtree balanced").
- **Preorder** = use it when a **child needs something computed by its ancestors** (a
  running path-sum, a depth counter) — information flows *down*, not up.
- **Inorder** on a BST specifically produces sorted output — save this one for Day-3-style
  BST problems.

## 5. Level-order BFS: the `level_size` fence

To emit levels as separate lists (not one flat list), you must snapshot the queue's length
*before* mutating it:

```python
from collections import deque

def level_order(root):
    if root is None:
        return []
    result, q = [], deque([root])
    while q:
        level_size = len(q)          # FENCE: freezes "this level" vs "children about to arrive"
        level = []
        for _ in range(level_size):
            node = q.popleft()
            level.append(node.val)
            if node.left  is not None: q.append(node.left)
            if node.right is not None: q.append(node.right)
        result.append(level)
    return result
```

If you write `while q:` for the inner loop instead of `for _ in range(level_size):`, the loop
keeps consuming nodes as you append their children — it drains the *entire tree* in one pass and
every level collapses into a single list. The snapshot is a fence: it freezes the boundary between
nodes already queued and children about to be added, so the inner loop processes exactly one
level.

**Second trap in the same function:** guard the empty-root case. `deque([None])` is non-empty, so
skipping the `if root is None: return []` guard leads straight to `None.val` raising
`AttributeError`. An empty tree is a legal input; every traversal needs this guard.

## 6. Minimum Depth: `min()` needs an absent-child guard; `max()`/`sum()` don't

The single most common trap in bottom-up tree recursion. The naive transfer from `height()`:

```python
def minDepth(root):              # WRONG on lopsided trees
    if root is None: return 0
    left, right = minDepth(root.left), minDepth(root.right)
    return min(left, right) + 1
```

Trace a node with a left child but **no right child**: `right = minDepth(None) = 0`. Then
`min(left, 0) + 1` always evaluates to `1`, no matter how deep the left subtree actually is — the
missing child's `0` masquerades as "I found a leaf right here," which is false; there is no node
there at all.

```python
def minDepth(root):              # CORRECT
    if root is None: return 0
    left, right = minDepth(root.left), minDepth(root.right)
    if left == 0:  return right + 1     # left child absent — must use the real side
    if right == 0: return left + 1      # right child absent — must use the real side
    return min(left, right) + 1
```

The general rule: **a `0` return can only mean "empty subtree"** (a real node always returns
`>= 1` here), so it doubles as an absence flag. `max()` and `sum()` are immune to this because the
*present* side always wins or contributes correctly regardless of what the absent side returns.
`min()` is the one aggregation where an absent child's placeholder value can wrongly win.

**Related interview tell:** "nearest / shallowest / fewest-steps-to-X" → reach for **BFS**, not
DFS. BFS explores in strict order of distance and can stop the instant it finds the target, so it
never has to explore a needlessly deep branch. DFS has no such early exit — a shallower answer
could be hiding anywhere, so it must explore everything. (Trade-off: BFS's queue can hold O(width)
nodes; DFS's stack is only O(height).)

## 7. Iterative traversal: recursion is a stack you can hold yourself

Recursion isn't magic — Python maintains a call stack of "unfinished business." Iterative
traversal makes that stack explicit as a list you manage by hand.

**Preorder is trivial** because it emits a node the instant it's met, before either child — there
is nothing to defer:

```python
def preorder_iter(root):
    if root is None: return []
    stack, out = [root], []
    while stack:
        node = stack.pop()
        out.append(node.val)
        if node.right is not None: stack.append(node.right)   # push right FIRST
        if node.left  is not None: stack.append(node.left)    # left LAST -> pops first
    return out
```

Rule: **push in the reverse of the order you want to pop** (stack = LIFO).

**Inorder and postorder must defer** a node's visit until after some/all of its children are
done, so you need a marker to say "I've met this node but I'm not allowed to emit it yet":

```python
def _marker_template(root, self_push_position):
    """self_push_position in {'first', 'middle', 'last'} among the three pushes."""
    if root is None: return []
    stack, out = [(root, False)], []
    while stack:
        node, ready = stack.pop()
        if ready:
            out.append(node.val)
            continue
        # push (node, True) at the chosen position, relative to right/left:
        pushes = []
        if node.right is not None: pushes.append((node.right, False))
        if node.left  is not None: pushes.append((node.left,  False))
        # pushes currently = [right?, left?]; splice the self-marker in
        if self_push_position == 'last':                       # -> preorder
            stack += pushes + [(node, True)]
        elif self_push_position == 'middle':                    # -> inorder
            if node.right is not None: stack.append((node.right, False))
            stack.append((node, True))
            if node.left  is not None: stack.append((node.left,  False))
        elif self_push_position == 'first':                     # -> postorder
            stack.append((node, True))
            if node.right is not None: stack.append((node.right, False))
            if node.left  is not None: stack.append((node.left,  False))
    return out
```

**The single unifying fact**, found by deliberately getting postorder wrong twice and reading what
each wrong output implied:

| `(node, True)` pushed at... | pops... | node emitted | order |
|---|---|---|---|
| **last** among the three pushes | first (LIFO) | before children | **preorder** |
| **middle** | middle | between children | **inorder** |
| **first** | last | after children | **postorder** |

Concretely, two failure modes worth knowing *because they're diagnostic*, not just "bugs to avoid":

- **Emit-on-wrong-branch:** if you emit on `not ready` instead of `ready` (branches flipped), the
  root prints immediately and its children are never pushed — output collapses to `[root.val]`
  and nothing else. If you see a single-element output where you expected the whole tree, check
  which branch emits vs. expands.
- **Self-push in the wrong slot:** branches correct, but `(node, True)` pushed *last* instead of
  *first* — you'll get a perfectly valid **preorder** traversal back while trying to write
  postorder. If your "postorder" output looks suspiciously like preorder, this is why.

## 8. `nonlocal` and the closure trap in bottom-up "track a side value" patterns

Some bottom-up problems need to *return* one thing to the parent while *also* tracking a second,
running answer that the parent never sees — diameter is the canonical example: each node returns
its height upward, but the true diameter (which may not pass through the root) has to be tracked
separately as a running maximum.

```python
def diameter_of_tree(root):
    def longest_path(node):
        if node is None:
            return -1
        left  = longest_path(node.left)
        right = longest_path(node.right)
        nonlocal dia                     # REQUIRED
        dia = max(dia, left + right + 2)  # posted aside — parent never sees this
        return max(left, right) + 1       # returned up — this is what the parent needs
    dia = 0
    longest_path(root)
    return dia
```

Drop `nonlocal dia` and Python raises `UnboundLocalError` the moment `longest_path` tries to
*read* `dia` on the line `dia = max(dia, ...)` — not because `dia` doesn't exist in an enclosing
scope, but because **an assignment to a name anywhere in a function body marks that name local for
the function's *entire* body**, including lines before the assignment. `nonlocal` is what tells
Python "no, reuse the enclosing scope's variable instead of shadowing it."

**Mnemonic for the whole pattern:** *return for the parent, post to the whiteboard.* One value
flows up through the return chain because the parent's own math needs it; a second value gets
posted to a shared whiteboard (the `nonlocal` variable) that only the outermost caller reads at
the end.

`isBalanced` is the same pattern with a boolean instead of a max:

```python
def isBalanced(root):
    def height(node):
        if node is None:
            return 0
        left, right = height(node.left), height(node.right)
        if abs(left - right) > 1:
            nonlocal ok
            ok = False
        return max(left, right) + 1
    ok = True
    height(root)
    return ok
```

## 9. Complexity trap: "repeat a traversal inside a recursion" is O(n²), not O(n log n)

A tempting *naive* balanced-tree check calls `height()` fresh at every node:

```python
def isBalanced_naive(node):
    if node is None: return True
    if abs(height(node.left) - height(node.right)) > 1:
        return False
    return isBalanced_naive(node.left) and isBalanced_naive(node.right)
```

It's easy to eyeball this as `O(n log n)` by analogy with balanced-tree bounds (`O(log n)`
levels, `O(n)` work per level) — but that analogy only holds if the tree actually *is* balanced.
On a **skewed/degenerate** tree (essentially a linked list), there are `O(n)` levels, and the
`height()` call at the node at depth `k` costs `O(n - k)`. Summed over all nodes that's
`(n-1) + (n-2) + ... + 1`, an arithmetic series — **O(n²)**, not `O(n log n)`.

Concretely, for `n = 1000`: `n log n ≈ 10,000`, but the actual work is `≈ 500,000` — a 50x gap.
Numbers like that are the fastest way to unstick a wrong complexity intuition; the general lesson
survives even where the specific numbers don't: **"call a full traversal from inside another
traversal" multiplies the two traversals' costs together in the worst case — check the *worst-case
shape* of the input (skewed, not balanced) before trusting a complexity intuition drawn from the
best case.**

The fix, unsurprisingly, is the bottom-up pattern from section 8 — compute height and check
balance in the **same** postorder pass, O(n) total.

## Summary table

| Trap | One-line fix |
|---|---|
| "Connected" alone isn't a tree | Also require acyclic / exactly N−1 edges |
| Child-count vs. graph-degree | Non-root node has 3 neighbours, ≤2 children |
| `if not node` | Use `if node is None` — immune to `__bool__`/`__len__` |
| Wrong traversal order | postorder = child-dependent; preorder = parent→child info flow |
| BFS levels merge into one | Snapshot `level_size = len(q)` before the inner loop |
| BFS crashes on empty tree | Guard `if root is None: return []` |
| Min Depth wrong on lopsided trees | Skip the child that returned `0` (absent), don't blindly `min()` |
| Iterative postorder comes out wrong | Self-push position: last=pre, middle=in, first=post |
| `UnboundLocalError` on a tracked global | Add `nonlocal` before any read-then-write on an outer var |
| "Repeated traversal in recursion" complexity | Assume worst case is a skewed tree, not a balanced one — check with concrete numbers |
