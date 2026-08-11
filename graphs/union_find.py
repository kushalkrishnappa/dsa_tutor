class UnionFind:

    def __init__(self):
        self.leader = {}
        self.size = {}

    def find(self, node: int) -> int:
        if node != self.leader.setdefault(node, node):
            self.leader[node] = self.find(self.leader[node])
        return self.leader[node]

    def union(self, node1: int, node2: int) -> bool:
        leader1 = self.find(node1)
        leader2 = self.find(node2)
        if leader1 != leader2:
            leader1_sz = self.size.setdefault(leader1, 1)
            leader2_sz = self.size.setdefault(leader2, 1)
            if leader1_sz >= leader2_sz:
                self.leader[leader2] = leader1
                self.size[leader1] += self.size[leader2]
            elif leader1_sz < leader2_sz:
                self.leader[leader1] = leader2
                self.size[leader2] += self.size[leader1]
            return True
        return False

edges = [(1, 2), (2, 3), (4, 5), (3, 4), (1, 5)]

uf = UnionFind()
for u, v in edges:
    print(u, v, uf.union(u, v))
print(uf.size[uf.find(1)])
