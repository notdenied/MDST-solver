from classes import Graph, Edge

from utils import get_arbitrary_ostov, get_vertex_degrees, is_connected, read_graph, max_vert_degree


class MDSTSolver:
    def __init__(self, gr: Graph) -> None:
        self.gr = gr

    def solve(self) -> Graph | None:
        '''
        Finds solution (if it exists) and returns it.
        '''

        if len(self.gr.edges_set) == 0 and len(self.gr.vertices) == 1:
            return self.gr

        if not is_connected(self.gr):
            return

        verts = self.gr.vertices
        edges = get_arbitrary_ostov(self.gr)
        edges_set = set(edges)
        assert len(edges) == len(edges_set)

        while True:
            degrees = get_vertex_degrees(Graph(verts, edges))
            max_degree = max(degrees.values())
            forbidden_verts = set([x for x in verts if degrees[x] == max_degree])
            coloring = self._make_coloring(verts, edges, forbidden_verts)

            improved = False
            for edge in self.gr.edges_set:
                if edge.v_to in forbidden_verts or edge.v_from in forbidden_verts or coloring[edge.v_to] == coloring[edge.v_from] or edge in edges_set or (edge.inverse() in edges_set):
                    continue

                if degrees[edge.v_from] < max_degree - 1:
                    v1_res = True
                    v1_improve = None
                else:
                    v1_res, v1_improve = self._get_local_improve(verts, edges, self.gr.edges_set, coloring, edge.v_from, degrees, max_degree)
                    if v1_improve:
                        edges.append(v1_improve[0])
                        edges_set.add(v1_improve[0])
                        edges.remove(v1_improve[1])
                        edges_set.remove(v1_improve[1])
                        improved = True
                        break
                if not v1_res:
                    continue

                if degrees[edge.v_to] < max_degree - 1:
                    v2_res = True
                    v2_improve = None
                else:
                    v2_res, v2_improve = self._get_local_improve(verts, edges, self.gr.edges_set, coloring, edge.v_to, degrees, max_degree)
                    if v2_improve:
                        edges.append(v2_improve[0])
                        edges_set.add(v2_improve[0])
                        edges.remove(v2_improve[1])
                        edges_set.remove(v2_improve[1])

                if not v2_res:
                    continue

                try:
                    to_remove = self._get_edge_to_remove(coloring, forbidden_verts, edge.v_from, edge.v_to, verts, edges)
                except ValueError:
                    break

                improved = True
                edges.append(edge)
                edges_set.add(edge)
                edges.remove(to_remove)
                edges_set.remove(to_remove)
                break

            if not improved:
                break

        return Graph(verts, edges)

    def _get_local_improve(self, verts, t_edges_list, all_edges_set, coloring, vert, degrees, max_degree):
        same_colored_verts = [x for x in verts if coloring[vert] == coloring[x]]
        same_colored_edges = []
        same_colored_edges_set = set(same_colored_edges)

        for edge in all_edges_set:
            if edge in same_colored_edges_set or coloring[edge.v_to] != coloring[vert] or coloring[edge.v_from] != coloring[vert]:
                continue

            if degrees[edge.v_to] == max_degree - 1 or degrees[edge.v_from] == max_degree - 1:
                continue

            path = self._get_path_between_verts(edge.v_from, edge.v_to, same_colored_verts, same_colored_edges)
            if vert in path:
                ind = path.index(vert)
                return True, (edge, Edge(path[ind], path[ind+1]))

        return False, None

    def _dfs_with_path(self, edges_dict, vert, used, prev):
        if used[vert]:
            return False

        used[vert] = True

        for edge in edges_dict[vert]:
            if self._dfs_with_path(edges_dict, edge, used, prev):
                prev[edge] = vert

        return True

    def _get_path_between_verts(self, v1, v2, verts, edges):
        used = {x: False for x in verts}
        prev = {}
        prev[v1] = -1

        edges_dict = {x: list() for x in verts}
        for edge in edges:
            edges_dict[edge.v_from].append(edge.v_to)
            edges_dict[edge.v_to].append(edge.v_from)

        self._dfs_with_path(edges_dict, v1, used, prev)

        if not used[v2]:
            return []

        path = [v2]
        cur = v2
        while True:
            pr = prev[cur]
            if pr == -1:
                break
            path.append(pr)
            cur = pr

        return path

    def _get_edge_to_remove(self, coloring, forbidden_verts, v1, v2, verts, edges) -> Edge:
        print()
        path = self._get_path_between_verts(v1, v2, verts, edges)

        for i in range(len(path) - 1):
            u1, u2 = path[i], path[i+1]
            if (coloring[u1] == coloring[v1] and u2 in forbidden_verts) or \
                    (coloring[u2] == coloring[v1] and u1 in forbidden_verts):
                return Edge(u1, u2)
            if (coloring[u1] == coloring[v2] and u2 in forbidden_verts) or \
                    (coloring[u2] == coloring[v2] and u1 in forbidden_verts):
                return Edge(u1, u2)

        raise ValueError

    def _dfs(self, coloring, edges_dict, vert, cur_color, forbidden_verts):
        if coloring[vert] == -1:
            coloring[vert] = cur_color
        else:
            return

        for edge in edges_dict[vert]:
            if edge.v_to not in forbidden_verts:
                self._dfs(coloring, edges_dict, edge.v_to, cur_color, forbidden_verts)

    def _make_coloring(self, verts, edges, forbidden_verts):
        coloring = {x: -1 for x in verts}
        edges_dict = {x: list() for x in verts}
        for edge in edges:
            edges_dict[edge.v_from].append(edge)
            edges_dict[edge.v_to].append(edge)

        cur_color = -1
        for vert in verts:
            if coloring[vert] == -1 and vert not in forbidden_verts:
                cur_color += 1
                self._dfs(coloring, edges_dict, vert, cur_color, forbidden_verts)

        return coloring


if __name__ == "__main__":
    gr = read_graph()
    solver = MDSTSolver(gr)
    sol = solver.solve()
    print(sol if sol is not None else "no mst in graph")
    if sol:
        print(max_vert_degree(sol))
