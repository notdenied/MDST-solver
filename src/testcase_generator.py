import random

from classes import TestCase, Edge


class Generator:
    def __init__(self, vertex_count: int = 0, edges_count: int = 0, seed: int = 42) -> None:
        self.v_cnt = vertex_count
        self.e_cnt = edges_count
        random.seed(seed)

    def generate(self):
        """
        Generate tests!
        """

        # step 0: if we can't generate a tree
        if self.e_cnt < self.v_cnt - 1:
            possible_edges = list()
            for v1 in range(1, self.v_cnt+1):
                for v2 in range(v1+1, self.v_cnt+1):
                    possible_edges.append((v1, v2))
            edges = []
            for _ in range(self.e_cnt):
                ind = random.randint(0, len(possible_edges)-1)
                edges.append(possible_edges.pop(ind))
            return TestCase(self.v_cnt, self.e_cnt, [Edge(x, y) for x, y in edges])

        # step 1: generate any tree
        verts = list()
        edges = list()

        verts.append(random.randint(1, self.v_cnt))

        for v in range(1, self.v_cnt + 1):
            if v in verts:
                continue

            to = random.choice(verts)
            edges.append((v, to))
            verts.append(v)

        # step 2: add other edges
        possible_edges = list()
        for v1 in range(1, self.v_cnt+1):
            for v2 in range(v1+1, self.v_cnt+1):
                if (v1, v2) not in edges and (v2, v1) not in edges:
                    possible_edges.append((v1, v2))

        for _ in range(self.e_cnt - self.v_cnt + 1):
            ind = random.randint(0, len(possible_edges)-1)
            edges.append(possible_edges.pop(ind))

        return TestCase(self.v_cnt, self.e_cnt, [Edge(x, y) for x, y in edges])
