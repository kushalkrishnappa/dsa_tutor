from collections import defaultdict, deque

def build_adjacency_list(num_nodes: int, edges: list[tuple]):
    adj = defaultdict(list)
    for i in range(num_nodes):
        adj[i] = []
    for edge in edges:
        start, end = edge
        adj[start].append(end)
        adj[end].append(start)
    return adj

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

def print_adjacency_list(graph: dict[list]):
    print("Adjacency List Representation of Graph")
    print_line()
    for ele in graph:
        print(f"{ele} -> ", end=" ")
        neighbours = graph[ele]
        for node in neighbours:
            print(node, end=" ")
        print()
    print_line()

def print_line():
    print("========================")

def flood_fill_recursive(grid: list[list[int]], row, col):
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    def dfs(grid, row, col):
        if grid[row][col] != 0:
            grid[row][col] = 0 # flood the cell
            # process the neighbors
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 0:
                    dfs(grid, nr, nc)
    dfs(grid=grid, row=row, col=col)

def flood_fill_iterative(grid: list[list[int]], row: int, col: int) -> None:
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    stack = [(row, col)]
    grid[row][col] = 0
    while stack:
        r, c = stack.pop()
        if grid[r][c] == 0: # check if flooded
            # process the neighbors
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 0:
                    stack.append((nr, nc))
                    grid[nr][nc] = 0 # flood the cell

# def has_cycle_directed(graph) -> bool:
#     ON_STACK = 1
#     DONE = 2

#     visited = set()
#     def dfs(node):
#         for neighbor in graph[node]:
#             # check if the neighbor is on stack
#             if (neighbor, ON_STACK) in visited:
#                 return True
#             if (neighbor, DONE) not in visited:
#                 visited.add((neighbor, ON_STACK))
#                 if dfs(neighbor):
#                     return True
#         visited.remove((node, ON_STACK))
#         visited.add((node, DONE))
#         return False
    
#     for node in graph:
#         if (node, DONE) not in visited:
#             visited.add((node, ON_STACK))
#             if dfs(node):
#                 return True
#     return False

from collections import defaultdict

def has_cycle_directed(graph) -> bool:
    NOT_EXPLORED, ON_STACK, DONE = 0, 1, 2
    status = defaultdict(int)
    def dfs(node: int) -> bool:
        status[node] = ON_STACK
        for nb in graph[node]:
            if status[nb] == ON_STACK: return True
            if status[nb] == NOT_EXPLORED and dfs(nb): return True
        status[node] = DONE
        return False
    return any(status[node] == NOT_EXPLORED and dfs(node) for node in graph)

def has_cycle_undirected(graph) -> bool:
    visited = set()
    def dfs(node: int, parent: int):
        # in undirected if node is visited then cycle
        if node in visited:
            return True
        visited.add(node)
        for nb in graph[node]:
            if nb != parent:
                if dfs(nb, node): return True
        return False
    return any(node not in visited and dfs(node=node, parent=-1) for node in graph)


def topological_sort(graph: dict[int, list]) -> list | None:
    # Khan's Algorithm
    # 1. calcualte the in-degree for each node
    # 2. Add all in-degree-0 nodes to the pool
    # 3. Pull from pool if poll not empty
    #       - add the node to order
    #       - decrese the in-degee of node's neighbors -= 1
    #       - Add all in-degree-0 nodes to the pool
    #                - if no node with in-degree-0 that's a cyclic dependency -> return None
    # if pool empty and len(order) < len(dict) -> return None
    pass

def is_valid_topo_order(graph: dict[int, list], order: list) -> bool:
    pass


if __name__ == "__main__":
    num_nodes = 6
    edges = [(1, 2), (1, 3), (1, 4), (2, 5), (3, 6), (4, 3), (5, 6)]
    graph = build_adjacency_list(num_nodes, edges)
    print_adjacency_list(graph)
    print(f"bfs: {bfs(graph, 1)}")
    print(f"dfs_recursive: {dfs_recursive(graph, 1)}")
    print(f"dfs_iterative: {dfs_iterative(graph, 1)}")


    # Grid: Flood Fill
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

    print()

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
    # ===============================================

    # Cycle Detection in Directed Graphs
    print()

    cyclic  = {0: [1], 1: [2], 2: [0], 3: [2]}      # 0→1→2→0   → expect True
    acyclic = {0: [1, 2], 1: [3], 2: [3], 3: []}    # diamond   → expect False
    print(f"Has cycle: {has_cycle_directed(cyclic)}")
    print(f"Has cycle: {has_cycle_directed(acyclic)}")

    # Cycle Detection in Undirected Graphs
    print()

    triangle = {0: [1, 2], 1: [0, 2], 2: [0, 1]}          # 0—1—2—0  → expect True
    tree     = {0: [1, 2], 1: [0, 3], 2: [0], 3: [1]}     # no loop  → expect False
    print(f"Has cycle undirected: {has_cycle_undirected(triangle)}")
    print(f"Has cycle undirected: {has_cycle_undirected(tree)}")
