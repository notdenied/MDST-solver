from itertools import combinations

from classes import Graph
from utils import is_connected, max_vert_degree, read_graph


class DummySolver:
    # Dummy Solver for correctness check
    def __init__(self, graph: Graph) -> None:
        self.gr = graph

    def solve(self) -> Graph | None:
        if len(self.gr.edges_set) == 0 and len(self.gr.vertices) == 1:
            return self.gr

        if not is_connected(self.gr):
            return

        verts = self.gr.vertices
        egdes_list = list(self.gr.edges_set)  # ironically

        best_degree = float('inf')
        best_graph = self.gr

        for egdes in combinations(egdes_list, len(verts) - 1):  # exp
            tmp_gr = Graph(verts, egdes)
            if is_connected(tmp_gr):
                degree = max_vert_degree(tmp_gr)
                if degree < best_degree:
                    best_degree = degree
                    best_graph = tmp_gr

        return best_graph


if __name__ == "__main__":
    gr = read_graph()
    solver = DummySolver(gr)
    sol = solver.solve()
    print(sol if sol is not None else "no mst in graph")
    if sol:
        print(max_vert_degree(sol))
