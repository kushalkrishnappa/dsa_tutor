"""

"""

from collections import defaultdict

EPS = 1e-9  # float tolerance, so 0.1 + 0.2 isn't flagged against 0.3


def find_over_allocated(nodes: dict[str, float], edges: list[tuple[str, str]]) -> list[str]:
    """
    Returns all node IDs whose direct children's budgets sum 
    to more than the node's own budget.
    e.g. ["eng"]
    """
    child_sum = defaultdict(float)
    for parent, child in edges:
        child_sum[parent] += nodes[child]
    return [p for p, total in child_sum.items() if total > nodes[p]]


def find_over_allocation_amounts(nodes: dict[str, float], edges: list[tuple[str, str]]) -> dict[str, float]:
    """
    Follow-up 1: maps each over-allocated node ID to how much its
    children's budgets exceed its own.
    e.g. {"eng": 50.0}
    """
    child_sum = defaultdict(float)
    for parent, child in edges:
        child_sum[parent] += nodes[child]
    return {p: total - nodes[p] for p, total in child_sum.items() if total > nodes[p]}


def find_over_allocated_dag(nodes: dict[str, float], edges: list[tuple[str, str, float]]) -> dict[str, float]:
    """
    Follow-up 2: DAG where parents split a child's funding. Each edge carries the parent's share.
    e.g. edges=[("eng", "ml", 0.5), ("research", "ml", 0.5)] -> each parent funds half of ml
    """
    child_sum = defaultdict(float)
    for parent, child, share in edges:
        child_sum[parent] += share * nodes[child]
    return {
        p: round(total - nodes[p], 3)
        for p, total in child_sum.items()
        if round(total, 3) > round(nodes[p], 3)
    }


class BudgetTracker:
    """
    Follow-up 3: O(1) per update and per lookup.
    A budget change only affects the node's own check and its parent's check.
    """

    def __init__(self, nodes: dict[str, float], edges: list[tuple[str, str]]):
        self.budget = dict(nodes)
        self.parent = {child: parent for parent, child in edges}
        self.child_sum = defaultdict(float)
        for parent, child in edges:
            self.child_sum[parent] += nodes[child]
        self.over = {p for p, total in self.child_sum.items() if total > nodes[p] + EPS}

    def _recheck(self, node: str) -> None:
        if self.child_sum[node] > self.budget[node] + EPS:
            self.over.add(node)
        else:
            self.over.discard(node)

    def update(self, node: str, new_budget: float) -> None:
        delta = new_budget - self.budget[node]
        self.budget[node] = new_budget
        self._recheck(node)                      # node's own budget vs its children
        if node in self.parent:
            p = self.parent[node]
            self.child_sum[p] += delta           # node's change hits its parent's total
            self._recheck(p)

    def is_over_allocated(self, node: str) -> bool:
        return node in self.over


def scale_down(nodes: dict[str, float], edges: list[tuple[str, str]]) -> dict[str, float]:
    """
    Follow-up 4: scale over-allocated children down proportionally.
    Fix a node's kids first, then let each kid fix its own kids.
    """
    children = defaultdict(list)
    for parent, child in edges:
        children[parent].append(child)
    budget = dict(nodes)

    def fix(node):
        kids = children[node]
        total = sum(budget[k] for k in kids)
        if total > budget[node]:
            for k in kids:
                budget[k] = budget[k] * budget[node] / total
        for k in kids:
            fix(k)

    root = None
    children_set = {child for _, child in edges}
    for node in nodes:
        if node not in children_set:
            root = node
            break
    fix(root)
    return budget


if __name__ == "__main__":
    nodes = {
        "root":    1000.0,
        "eng":      600.0,
        "design":   300.0,
        "frontend": 250.0,
        "backend":  400.0,
        "ux":       150.0,
        "brand":    100.0,
    }

    edges = [
        ("root",   "eng"),
        ("root",   "design"),
        ("eng",    "frontend"),
        ("eng",    "backend"),
        ("design", "ux"),
        ("design", "brand"),
    ]

    print(find_over_allocated(nodes, edges))
    print(find_over_allocation_amounts(nodes, edges))

    dag_nodes = {"root": 1000.0, "eng": 300.0, "research": 300.0, "ml": 400.0}
    dag_edges = [("root", "eng", 1.0), ("root", "research", 1.0), ("eng", "ml", 0.8), ("research", "ml", 0.2)]
    print(find_over_allocated_dag(dag_nodes, dag_edges))

    tracker = BudgetTracker(nodes, edges)
    print(tracker.over)
    tracker.update("eng", 700.0)
    print(tracker.over)
    tracker.update("design", 450.0)
    print(tracker.over)

    print(scale_down(nodes, edges))
