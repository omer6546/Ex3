from src.Node import Node
import random
from src.GraphInterface import GraphInterface


class DiGraph(GraphInterface):
    def __init__(self):
        self.size = 0
        self.nodedict = {}
        self.edgedict = {}
        self.mc = 0

    def __repr__(self):
        return 'Graph: ' + '|V|=' + str(self.v_size()) + ' , ' + '|E|=' + str(self.e_size())

    def v_size(self) -> int:
        return len(self.nodedict)

    def e_size(self) -> int:
        c = 0
        for src, edge in self.edgedict.items():
            c += len(edge)
        return c

    def get_all_v(self) -> dict:
        return self.nodedict

    def all_in_edges_of_node(self, id1: int) -> dict:
        ans = {}
        if id1 not in self.nodedict or self is None:
            return ans
        for key in self.edgedict:
            if key != id1:
                if id1 in self.edgedict[key].keys():
                    ans[key] = self.edgedict[key][id1]
        return ans

    def all_out_edges_of_node(self, id1: int) -> dict:
        return self.edgedict[id1]

    def get_mc(self) -> int:
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if id1 != id2 and id1 in self.nodedict and id2 in self.nodedict:
            if id1 not in self.edgedict:
                self.edgedict[id1] = {id2: weight}
            else:
                if id2 not in self.edgedict[id1]:
                    self.edgedict[id1][id2] = weight
                else:
                    return False
            self.mc += 1
            return True
        else:
            return False

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if node_id not in self.nodedict:
            if pos is None:
                pos = (random.random() * 40, random.random() * 40, 0.0)
            n = Node(node_id, pos)
            self.nodedict[node_id] = n
            self.mc += 1
            return True
        return False

    def remove_node(self, node_id: int) -> bool:
        if node_id not in self.nodedict:
            return False
        del self.nodedict[node_id]
        del self.edgedict[node_id]
        for key in self.edgedict:
            if node_id in self.edgedict[key].keys():
                del self.edgedict[key][node_id]
        self.mc += 1
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if node_id1 != node_id2 and node_id1 in self.nodedict and node_id2 in self.nodedict and node_id2 in \
                self.edgedict[node_id1]:
            del self.edgedict[node_id1][node_id2]
            self.mc += 1
            return True
        return False


def main():
    pos = (1, 2, 3)
    g = DiGraph()
    print(g.add_node(1, pos))
    n = g.nodedict[1]
    print(n.get_key)
    print(g.add_node(2))
    print(g.add_node(3))
    print(g.add_edge(1, 2, 3.5))
    print(g.add_edge(2, 1, 4.5))
    print(g.add_edge(1, 3, 1.5))
    print(g.add_edge(3, 2, 7.5))
    print(g.nodedict[1])
    print(g.nodedict[2])
    print(g.edgedict)
    print(g.all_out_edges_of_node(2))
    print(g.all_in_edges_of_node(2))
    print(g.remove_edge(3, 2))
    print(g.edgedict)
    print(g.add_edge(3, 2, 7.5))
    print(g.edgedict)
    print(g.get_all_v())


if __name__ == '__main__':
    main()
