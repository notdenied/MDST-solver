from dataclasses import dataclass


@dataclass
class Edge:
    v_from: int
    v_to: int

    def to_str(self):
        return f"{self.v_from} {self.v_to}"

    def __str__(self) -> str:
        return self.to_str()

    def __hash__(self) -> int:
        return hash((min(self.v_from, self.v_to), max(self.v_from, self.v_to)))

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Edge):
            raise ValueError
        return min(self.v_from, self.v_to) == min(value.v_from, value.v_to) and \
            max(self.v_from, self.v_to) == max(value.v_from, value.v_to)

    def inverse(self):
        return Edge(self.v_to, self.v_from)


@dataclass
class Graph:
    # very bad, but...
    vertices: set[int]
    edges: dict[int, list[int]]
    edges_set: set[Edge]

    def __init__(self, vertices: list[int] | set[int], edges_list: list[Edge] | tuple[Edge, ...]):
        self.vertices = set(vertices)
        self.edges_set = set(edges_list)
        self.edges = {x: list() for x in self.vertices}
        for edge in edges_list:
            self.edges[edge.v_from].append(edge.v_to)
            self.edges[edge.v_to].append(edge.v_from)

    def __str__(self):
        out = f'''{len(self.vertices)} {len(self.edges_set)}
{" ".join(map(str, self.vertices))}
{'\n'.join(map(str, self.edges_set))}'''
        return out


@dataclass
class TestCase:
    vert_cnt: int
    edges_cnt: int
    edges: list[Edge]

    def to_str(self):
        return f"{self.vert_cnt} {self.edges_cnt}\n" + \
            ' '.join([str(i) for i in range(1, self.vert_cnt+1)]) + '\n' + \
            '\n'.join([i.to_str() for i in self.edges])

    def to_graph(self):
        return Graph(list(range(1, self.vert_cnt+1)), self.edges)
