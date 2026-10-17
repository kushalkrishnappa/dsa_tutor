"""Minimum Spanning Tree."""


class UnionFind:

    def __init__(self, size):
        self.size = {i: 1 for i in range(size)}
        self.leader = {i : i for i in range(size)}

    def find(self, node: int) -> int:
        """Find the parent of the node."""
        if self.leader[node] != node:
            self.leader[node] = self.find(self.leader[node])
        return self.leader[node]

    def union(self, n1: int, n2: int) -> bool:
        """Connect two nodes. If they have different leader merge groups."""
        leader1 = self.find(n1)
        leader2 = self.find(n2)
        if leader1 != leader2:
            # union by size
            if self.size[leader1] > self.size[leader2]:
                self.leader[leader2] = leader1
                self.size[leader1] += self.size[leader2]
            else:
                self.leader[leader1] = leader2
                self.size[leader2] += self.size[leader1]
            return True
        return False


def mst_kruskels():
    pass