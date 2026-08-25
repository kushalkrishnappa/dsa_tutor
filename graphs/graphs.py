from collections import defaultdict, deque
from utils import print_line, print_topic

#############################################
print_topic("Graph Representation & Traversal")
#############################################


def build_adjacency_list(num_nodes: int, edges: list[tuple]):
    adj = defaultdict(list)
    for i in range(num_nodes):
        adj[i] = []
    for edge in edges:
        start, end = edge
        adj[start].append(end)
        adj[end].append(start)
    return adj


num_nodes = 6
edges = [(1, 2), (1, 3), (1, 4), (2, 5), (3, 6), (4, 3), (5, 6)]
graph = build_adjacency_list(num_nodes, edges)
print(f"build_adjacency_list: {dict(graph)}")
print_line()


def bfs(graph: dict[list], start: int) -> list:
    bfs_order = []
    queue = deque([start])
    visited = set([start])
    while queue:
        node = queue.popleft()
        neighbors = graph[node]
        for nbhr in neighbors:
            if nbhr not in visited:
                visited.add(nbhr)
                queue.append(nbhr)
        bfs_order.append(node)
    return bfs_order


print(f"bfs: {bfs(graph, 1)}")
print_line()


def dfs_recursive(graph: dict[list], start: int):
    dfs_order = [start]
    visited = set([start])

    def dfs(start):
        neighbors = graph[start]
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                dfs_order.append(neighbor)
                dfs(neighbor)

    dfs(start)
    return dfs_order


print(f"dfs_recursive: {dfs_recursive(graph, 1)}")
print_line()


def dfs_iterative(graph: dict[list], start: int):
    dfs_order = []
    stack = [start]
    visited = set([start])
    while stack:
        node = stack.pop()
        neighbors = graph[node]
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)
        dfs_order.append(node)
    return dfs_order


print(f"dfs_iterative: {dfs_iterative(graph, 1)}")
print_line()


def print_adjacency_list(graph: dict[list]):
    print("Adjacency List Representation of Graph")
    print_line()
    for ele in graph:
        print(f"{ele} -> ", end=" ")
        neighbours = graph[ele]
        for node in neighbours:
            print(node, end=" ")
        print()


print_adjacency_list(graph)

#############################################
print_topic("Flood Fill")
#############################################


def flood_fill_recursive(grid: list[list[int]], row, col):
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def dfs(grid, row, col):
        if grid[row][col] != 0:
            grid[row][col] = 0  # flood the cell
            # process the neighbors
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 0:
                    dfs(grid, nr, nc)

    dfs(grid=grid, row=row, col=col)


print("flood_fill_recursive:")
grid = [
    [1, 1, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 1],
    [0, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 1, 0],
    [1, 0, 0, 0, 1, 0],
]
flood_fill_recursive(grid=grid, row=0, col=0)
for row in grid:
    print(row)
print_line()


def flood_fill_iterative(grid: list[list[int]], row: int, col: int) -> None:
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    stack = [(row, col)]
    grid[row][col] = 0
    while stack:
        r, c = stack.pop()
        if grid[r][c] == 0:  # check if flooded
            # process the neighbors
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 0:
                    stack.append((nr, nc))
                    grid[nr][nc] = 0  # flood the cell


print("flood_fill_iterative:")
grid = [
    [1, 1, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 1],
    [0, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 1, 0],
    [1, 0, 0, 0, 1, 0],
]
flood_fill_iterative(grid=grid, row=0, col=0)
for row in grid:
    print(row)

#############################################
print_topic("Cycle Detection")
#############################################


def has_cycle_directed(graph) -> bool:
    NOT_EXPLORED, ON_STACK, DONE = 0, 1, 2
    status = defaultdict(int)

    def dfs(node: int) -> bool:
        status[node] = ON_STACK
        for nb in graph[node]:
            if status[nb] == ON_STACK:
                return True
            if status[nb] == NOT_EXPLORED and dfs(nb):
                return True
        status[node] = DONE
        return False

    return any(status[node] == NOT_EXPLORED and dfs(node) for node in graph)


cyclic = {0: [1], 1: [2], 2: [0], 3: [2]}  # 0→1→2→0   → expect True
acyclic = {0: [1, 2], 1: [3], 2: [3], 3: []}  # diamond   → expect False
print(f"has_cycle_directed: Cyclic: {has_cycle_directed(cyclic)}")
print(f"has_cycle_directed: Acyclic: {has_cycle_directed(acyclic)}")
print_line()


def has_cycle_undirected(graph) -> bool:
    visited = set()

    def dfs(node: int, parent: int):
        # in undirected if node is visited then cycle
        if node in visited:
            return True
        visited.add(node)
        for nb in graph[node]:
            if nb != parent:
                if dfs(nb, node):
                    return True
        return False

    return any(node not in visited and dfs(node=node, parent=-1) for node in graph)


triangle = {0: [1, 2], 1: [0, 2], 2: [0, 1]}  # 0—1—2—0  → expect True
tree = {0: [1, 2], 1: [0, 3], 2: [0], 3: [1]}  # no loop  → expect False
print(f"has_cycle_undirected: Triangle: {has_cycle_undirected(triangle)}")
print(f"has_cycle_undirected: Tree: {has_cycle_undirected(tree)}")

#############################################
print_topic("Topological Sort")
#############################################


def topological_sort(graph: dict[int, list]) -> list | None:
    """Khan's Algorithm
    1. calcualte the in-degree for each node
    2. Add all in-degree-0 nodes to the pool
    3. Pull from pool if poll not empty
        - add the node to order
        - decrease the in-degee of node's neighbors -= 1
        - add all in-degree-0 nodes to the pool
        - if no node with in-degree-0
            = cyclic dependency -> return None
    4. if pool empty and len(order) < len(dict)
        = cyclic dependency -> return None
    """
    topo_order = []
    in_degree_list = {}

    # calculate indegree
    for node in graph:
        in_degree_list[node] = 0
    for nbrs in graph.values():
        for nb in nbrs:
            in_degree_list[nb] += 1

    # add all in-degree-0 nodes to the pool
    zero_in_degree_queue = deque([])
    for node, in_degree in in_degree_list.items():
        if in_degree == 0:
            zero_in_degree_queue.append(node)

    while zero_in_degree_queue:
        node = zero_in_degree_queue.popleft()
        topo_order.append(node)
        for nb in graph[node]:
            in_degree_list[nb] -= 1
            if in_degree_list[nb] == 0:
                zero_in_degree_queue.append(nb)

    if len(topo_order) != len(graph):
        return None
    return topo_order


acyclic = {0: [1, 2], 1: [3], 2: [3], 3: []}  # expect a valid order
cyclic = {0: [1], 1: [2], 2: [0], 3: [2]}  # expect None
print(f"Topological Sort: Acyclic: {topological_sort(acyclic)}")
print(f"Topological Sort: Cyclic: {topological_sort(cyclic)}")
relabeled = {1: [2, 3], 2: [4], 3: [4], 4: []}  # node start from 1 and not 0
print(f"Topological Sort: Relabeled 1-indexed: {topological_sort(relabeled)}")
print_line()


def is_valid_topo_order(graph: dict[int, list], order: list) -> bool:
    if len(graph) != len(order):
        return False
    order_map = {}
    for idx, node in enumerate(order):
        order_map[node] = idx
    for node in graph:
        nbrs = graph[node]
        for nb in nbrs:
            if order_map[node] > order_map[nb]:
                return False
    return True


print(f"Valid Topo Order: {is_valid_topo_order(acyclic, [0, 1, 2, 3])}")  # True
print(f"Valid Topo Order: {is_valid_topo_order(acyclic, [0, 2, 1, 3])}")  # True
print(f"Valid Topo Order: {is_valid_topo_order(acyclic, [2, 0, 1, 3])}")  # False
print(f"Valid Topo Order: {is_valid_topo_order(relabeled, [1, 2, 3, 4])}")  # True
print(f"Valid Topo Order: {is_valid_topo_order(relabeled, [1, 2, 4, 3])}")  # False
print_line()


def topological_sort_dfs(graph: dict[int, list]) -> list | None:
    def dfs(node):
        status[node] = ON_STACK
        for nb in graph[node]:
            if status[nb] == ON_STACK:
                return True
            if status[nb] == NOT_EXPLORED and dfs(nb):
                return True
        status[node] = DONE
        topo_order.append(node)
        return False

    topo_order, status = [], defaultdict(int)
    NOT_EXPLORED, ON_STACK, DONE = 0, 1, 2
    if any(status[node] == NOT_EXPLORED and dfs(node) for node in graph):
        return None
    return topo_order[::-1]


print(f"Topological Sort DFS: Acyclic: {topological_sort_dfs(acyclic)}")
print(f"Topological Sort DFS: Cyclic: {topological_sort_dfs(cyclic)}")
print_line()
