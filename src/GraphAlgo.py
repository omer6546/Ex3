import sys
from typing import List
from src.GraphInterface import GraphInterface
from src.GraphAlgoInterface import GraphAlgoInterface
from src.DiGraph import DiGraph
from queue import PriorityQueue
import json
import matplotlib.pyplot as plt
import random
import time


class GraphAlgo(GraphAlgoInterface):
    def __init__(self, graph=None):
        self.graph = graph

    def get_graph(self) -> GraphInterface:
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        with open(file_name) as f:
            data = json.load(f)
            g = DiGraph()
            for node in data['Nodes']:
                g.add_node(node['id'])
                n = g.nodedict[node['id']]
                if 'pos' not in node:
                    st = str(random.random() * 40)+','+str(random.random() * 40)+','+str(random.random() * 40)
                else:
                    st = node['pos']
                pos_list = st.split(",")
                n.set_pos(float(pos_list[0]), float(pos_list[1]), float(pos_list[2]))
            for edge in data['Edges']:
                g.add_edge(edge['src'], edge['dest'], float(edge['w']))
            self.graph = g
            return True
        return False

    def save_to_json(self, file_name: str) -> bool:
        data = {"Edges": [], "Nodes": []}
        for key, node in self.get_graph().nodedict.items():
            x, y, z = node.pos
            x = str(x)
            y = str(y)
            z = str(z)
            data["Nodes"].append({"pos": x + "," + y + "," + z, "Id": key})
            if key in self.get_graph().edgedict:
                for dest, weight in self.get_graph().edgedict[key].items():
                    data["Edges"].append({"src": key, "w": str(weight), "dest": dest})
        with open(file_name, 'w') as f:
            json.dump(data, f)
            return True
        return False

    def dfs(self, node_id: int, graph: DiGraph):
        n = graph.nodedict[node_id]
        if n.info != "v":
            n.set_info("v")
            if node_id in graph.edgedict:
                for ni in graph.all_out_edges_of_node(node_id):
                    self.dfs(ni, graph)

    def reversed_copy(self) -> DiGraph:
        g = DiGraph()
        for node in self.get_graph().nodedict:
            g.add_node(node)
        for node in g.nodedict:
            if node in self.get_graph().edgedict:
                for ni in self.get_graph().all_out_edges_of_node(node):
                    g.add_edge(ni, node, 0)
        return g

    def is_in_q(self, q, key) -> bool:
        queue = q
        qlist = queue.queue
        for node in qlist:
            if node.key == key:
                return True
        return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        if id1 not in self.get_graph().nodedict or id2 not in self.get_graph().nodedict:
            return float('inf'), []
        parents = {}
        q = PriorityQueue()
        n = self.get_graph().nodedict[id1]
        n.set_weight(0)
        q.put(n)
        while not q.empty():
            curr = q.get()
            if curr.get_info != "v":
                curr.set_tag("v")
                if curr.key == id2:
                    break
            if curr.key in self.get_graph().edgedict:
                for ni, weight in self.get_graph().all_out_edges_of_node(curr.key).items():
                    node = self.get_graph().nodedict[ni]
                    if weight + curr.weight < node.weight:
                        node.set_weight(weight + curr.weight)
                        if ni in parents:
                            del parents[ni]
                        parents[ni] = curr.key
                        if not self.is_in_q(q, node.key):
                            q.put(node)
        path = []
        if not parents or id2 not in parents:
            return float('inf'), []
        if self.get_graph().nodedict[id2].weight == sys.float_info.max:
            return float('inf'), []
        assemble = id2
        while assemble != id1:
            path.append(self.get_graph().nodedict[assemble].key)
            assemble = parents[assemble]
        path.append(id1)
        path.reverse()
        ans = self.get_graph().nodedict[id2].weight
        for key, node in self.get_graph().nodedict.items():
            node.set_info(" ")
            node.set_weight(sys.float_info.max)
        return ans, path

    def connected_component(self, id1: int) -> list:
        if self.get_graph() is None or id1 not in self.get_graph().nodedict:
            return []
        self.dfs(id1, self.get_graph())
        ans = []
        com1 = []
        com2 = []
        for key, node in self.get_graph().nodedict.items():
            if node.info == "v":
                com1.append(node.key)
        g = self.reversed_copy()
        self.dfs(id1, g)
        for key, node in g.nodedict.items():
            if node.info == "v":
                com2.append(node.key)
        for node in com1:
            if node in com2:
                ans.append(node)
        for key, node in self.get_graph().nodedict.items():
            node.set_info(" ")
        return ans

    def connected_components(self) -> List[list]:
        if self.get_graph() is None:
            return []
        c = True
        ans = []
        for node in self.get_graph().nodedict.keys():
            flag = True
            if c:
                ans.append(self.connected_component(node))
                c = False
            else:
                for comp in ans:
                    if node in comp:
                        flag = False
                        break
                if flag:
                    ans.append(self.connected_component(node))
        return ans

    def plot_graph(self) -> None:
        x_val = []
        y_val = []
        keys = []
        for key, node in self.get_graph().nodedict.items():
            if node.pos[0] == 0.0 and node.pos[1] == 0.0:
                node.pos[0] = random.random() * 40
                node.pos[1] = random.random() * 40
            keys.append(key)
            x_val.append(node.pos[0])
            y_val.append(node.pos[1])

        for key, node in self.get_graph().nodedict.items():
            for dest, w in self.get_graph().edgedict[key].items():
                dx = self.get_graph().nodedict[dest].pos[0]
                dy = self.get_graph().nodedict[dest].pos[1]
                plt.arrow(self.get_graph().nodedict[key].pos[0], self.get_graph().nodedict[key].pos[1], dx-self.get_graph().nodedict[key].pos[0], dy-self.get_graph().nodedict[key].pos[1])
            # if node.pos[0] == 0.0 and node.pos[1] == 0.0:
            #     node.pos[0] = random.random() * 40
            #     node.pos[1] = random.random() * 40
            # keys.append(key)
            # x_val.append(node.pos[0])
            # y_val.append(node.pos[1])
        fig, ax = plt.subplots()
        ax.scatter(x_val, y_val)
        for i, txt in enumerate(keys):
            ax.annotate(keys[i], (x_val[i], y_val[i] + 0.05))

        plt.show()
        return None


def main():
    # pos = (1, 2, 3)
    g = DiGraph()
    # g.add_node(1, pos)
    # g.add_node(2)
    # g.add_node(3)
    # g.add_node(4)
    # g.add_node(5)
    # g.add_node(6)
    # g.add_edge(1, 2, 3)
    # g.add_edge(1, 3, 2)
    # g.add_edge(2, 5, 3)
    # g.add_edge(3, 1, 1)
    # g.add_edge(3, 4, 2)
    # g.add_edge(4, 3, 1)
    # g.add_edge(4, 5, 1)
    # g.add_edge(6, 5, 1)
    # g.add_edge(5, 6, 1)
    ga = GraphAlgo(g)
    # print(ga.shortest_path(1, 5))
    # print(ga.connected_component(1))
    # print(ga.connected_components())
    # print(g.edgedict)
    print(ga.load_from_json('../data/G_10_80_1.json'))
    start_time = time.time()
    print("start time: " + str(start_time))
    print(ga.shortest_path(1, 8))
    end_time = time.time()
    print("end time: " + str(end_time))
    duration = end_time - start_time
    print(duration)
    # ga.save_to_json('data/graph.json')
    # ga.plot_graph()


if __name__ == '__main__':
    main()
