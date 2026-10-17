"""Bipartite Graphs Algorithm.

Invariant: When a graph is bipartite, it has no odd-length cycle.
"""
from utils import print_line, print_topic
from collections import deque

#############################################
print_topic("Graph Representation & Traversal")
#############################################

def isBipartite(graph: dict[int, list]) -> bool:
    RED, BLUE = 0, 1
    queue = deque([])
    visited = set()
    color = {}

    def bfs(node):
        queue.append(node)
        visited.add(node)
        color[node] = RED
        while queue:
            curr_node = queue.popleft()
            for nb in graph[curr_node]:
                # case-1: color[nb] == color
                if color.get(nb, -1) == color[curr_node]:
                    return False
                # case-2: different color than node
                elif color.get(nb, -1) == 1 - color[curr_node]:
                    continue
                # case-3: assign color
                else:
                    color[nb] = 1 - color[curr_node]
                visited.add(nb)
                queue.append(nb)
        return True

    if all((node in visited) or bfs(node) for node in graph):
        return True
    return False

# tests
square = {0:[1,3],1:[0,2],2:[1,3],3:[0,2]}
print(f"Bipartite Graph: True: {isBipartite(square)}")

triangle = {0:[1,2],1:[0,2],2:[0,1]}
print(f"Bipartite Graph: False: {isBipartite(triangle)}")
print_line()

def isBipartiteRecursive(graph: dict[int, list]) -> bool:
    RED, BLUE = 0, 1
    visited = set()
    color = {}

    def bfs(node, clr):
        visited.add(node)
        color[node] = clr
        for nb in graph[node]:
            # case-1: color[nb] == color
            if color.get(nb, -1) == color[node]:
                return False
            # case-2: different color than node
            elif color.get(nb, -1) == 1 - color[node]:
                continue
            # case-3: assign color
            else:
                color[nb] = 1 - color[node]
            visited.add(nb)
            bfs(nb, 1 - color[node])
        return True

    if all((node in visited) or bfs(node, RED) for node in graph):
        return True
    return False

# tests
square = {0:[1,3],1:[0,2],2:[1,3],3:[0,2]}
print(f"Bipartite Graph: True: {isBipartiteRecursive(square)}")

triangle = {0:[1,2],1:[0,2],2:[0,1]}
print(f"Bipartite Graph: False: {isBipartiteRecursive(triangle)}")
print_line()