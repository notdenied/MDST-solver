from classes import Graph, Edge


def bfs(gr: Graph, used: dict[int, bool], vert: int, ostov_egdes: list) -> bool:
    if used[vert]:
        return False

    used[vert] = True
    for x in gr.edges[vert]:
        if bfs(gr, used, x, ostov_egdes):
            ostov_egdes.append(Edge(vert, x))

    return True


def get_arbitrary_ostov(gr: Graph) -> list[Edge]:
    used = {x: False for x in (gr.vertices)}
    ostov_edges = []

    bfs(gr, used, next(iter(gr.vertices)), ostov_edges)

    return ostov_edges


def is_connected(gr: Graph) -> bool:
    used = {x: False for x in (gr.vertices)}
    ostov_edges = []

    bfs(gr, used, next(iter(gr.vertices)), ostov_edges)

    return all(used.values())


def get_vertex_degrees(gr: Graph, forbidden_verts: set = set()):
    counters = {x: 0 for x in gr.vertices}

    for egde in gr.edges_set:
        if egde.v_to in forbidden_verts or egde.v_from in forbidden_verts:
            continue

        counters[egde.v_from] += 1
        counters[egde.v_to] += 1

    return counters


def max_vert_degree(gr: Graph) -> int:
    return max(get_vertex_degrees(gr).values())


def read_graph():
    _, m = map(int, input().split())
    verts = list(map(int, input().split()))
    edges = []
    for _ in range(m):
        edges.append(Edge(*map(int, input().split())))
    return Graph(verts, edges)
