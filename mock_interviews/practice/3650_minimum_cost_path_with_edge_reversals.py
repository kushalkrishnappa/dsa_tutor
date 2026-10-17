"""
Questions:
start = 0
end = n - 1
- min cost path = dikstras
- edge reversal = it makes sense to reverse an edge
going outwards from destination node.
- do I mandatority have to reverse the edge or is it okay if
I don're reverse and find the min cost path?
"""

"""
Approach:
- create a map for node -> smallest indegree weights
- standard dikstars + at each node also consider an extra
indegree weight.
Time: O(V + E)
Space: O(V + E)
"""

def min_cost(n: int, edges: list[list[int]]) -> int:
    pass