import sys
from typing import List
from src.GraphInterface import GraphInterface
from src.GraphAlgoInterface import GraphAlgoInterface
from src.DiGraph import DiGraph
from queue import PriorityQueue
from queue import Queue
import json
import matplotlib.pyplot as plt
import random
import time


class GraphAlgo(GraphAlgoInterface):
    def __init__(self, graph=None):
        self.graph = graph

    def get_graph(self) -> GraphInterface:
        return self.graph
    """
            :return: the directed graph on which the algorithm works on.
            """

    def load_from_json(self, file_name: str) -> bool:
        try:
            with open(file_name) as f:
                data = json.load(f)
                g = DiGraph()
                for node in data['Nodes']:
                    g.add_node(node['id'])
                    n = g.nodedict[node['id']]
                    if 'pos' not in node:
                        st = str(random.random() * 40) + ',' + str(random.random() * 40) + ',' + str(random.random() * 40)
                    else:
                        st = node['pos']
                    pos_list = st.split(",")
                    n.set_pos(float(pos_list[0]), float(pos_list[1]), float(pos_list[2]))
                for edge in data['Edges']:
                    g.add_edge(edge['src'], edge['dest'], float(edge['w']))
                self.graph = g
                return True
        except IOError:
            return False
    """
            Loads a graph from a json file.
            @param file_name: The path to the json file
            @returns True if the loading was successful, False o.w.
            """

    def save_to_json(self, file_name: str) -> bool:
        try:
            data = {"Edges": [], "Nodes": []}
            for key, node in self.get_graph().nodedict.items():
                x, y, z = node.pos
                x = str(x)
                y = str(y)
                z = str(z)
                data["Nodes"].append({"pos": x + "," + y + "," + z, "id": key})
                if key in self.get_graph().edgedict:
                    for dest, weight in self.get_graph().edgedict[key].items():
                        data["Edges"].append({"src": key, "w": str(weight), "dest": dest})
            with open(file_name, 'w') as f:
                json.dump(data, f)
                return True
        except IOError:
            return False
    """
            Saves the graph in JSON format to a file
            @param file_name: The path to the out file
            @return: True if the save was successful, False o.w.
            """

    def bfs(self, node_id: int, graph: DiGraph):
        q = Queue()
        n = graph.nodedict[node_id]
        q.put(n)
        n.set_tag(1)
        while not q.empty():
            node = q.get()
            if node.key in graph.edgedict:
                for key, w in graph.all_out_edges_of_node(node.key).items():
                    curr = graph.nodedict[key]
                    if curr.tag == 0:
                        q.put(curr)
                        curr.set_tag(1)
    """
              iterating over a given graph to perform a Breadth First Search Algorithm
              @param node_id: the start node key
              @param graph: the DiGraph we want to explore
              
              """

    def reversed_copy(self) -> DiGraph:
        g = DiGraph()
        for node in self.get_graph().nodedict:
            g.add_node(node)
        for node in g.nodedict:
            if node in self.get_graph().edgedict:
                for ni in self.get_graph().all_out_edges_of_node(node):
                    g.add_edge(ni, node, 0)
        return g
    """
                copy and reverses the given graph.
                returns a copy of the graph reversed.
                """

    def is_in_q(self, q, key) -> bool:
        queue = q
        qlist = queue.queue
        for node in qlist:
            if node.key == key:
                return True
        return False
    """
            checks if node is in priority queue.
            @param q: the priority queue
            @param key: the node id
            @returns True if node is in priority queue, False o.w.
            """

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
            if curr.get_tag != 1:
                curr.set_tag(1)
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
            node.set_tag(0)
            node.set_weight(sys.float_info.max)
        return ans, path
    """
          Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
          @param id1: The start node id
          @param id2: The end node id
          @return: The distance of the path, a list of the nodes ids that the path goes through
          If there is no path between id1 and id2, or one of them dose not exist the function returns (float('inf'),[])
        More info:
        https://en.wikipedia.org/wiki/Dijkstra's_algorithm
        """

    def connected_component(self, id1: int) -> list:
        if self.get_graph() is None or id1 not in self.get_graph().nodedict:
            return []
        self.bfs(id1, self.get_graph())
        ans = []
        com1 = []
        com2 = []
        for key, node in self.get_graph().nodedict.items():
            if node.tag == 1:
                com1.append(node.key)
        g = self.reversed_copy()
        self.bfs(id1, g)
        for key, node in g.nodedict.items():
            if node.tag == 1:
                com2.append(node.key)
        for node in com1:
            if node in com2:
                ans.append(node)
        for key, node in self.get_graph().nodedict.items():
            node.set_tag(0)
        return ans
    """
           Finds the Strongly Connected Component(SCC) that node id1 is a part of.
           @param id1: The node id
           @return: The list of nodes in the SCC
           Notes:
           If the graph is None or id1 is not in the graph, the function should return an empty list []
           """

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
    """
           Finds all the Strongly Connected Component(SCC) in the graph.
           @return: The list all SCC
           Notes:
           If the graph is None the function should return an empty list []
           """

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
        fig, ax = plt.subplots()
        ax.scatter(x_val, y_val, 50, "red")
        for src, node in self.get_graph().nodedict.items():
            if src in self.get_graph().edgedict:
                for dest, w in self.get_graph().edgedict[src].items():
                    dx = self.get_graph().nodedict[dest].pos[0]
                    dy = self.get_graph().nodedict[dest].pos[1]
                    plt.arrow(self.get_graph().nodedict[src].pos[0], self.get_graph().nodedict[src].pos[1], dx-self.get_graph().nodedict[src].pos[0], dy-self.get_graph().nodedict[src].pos[1], )
        for i, txt in enumerate(keys):
            ax.annotate(keys[i], (x_val[i], y_val[i] + 0.05))

        plt.show()
        return None
    """Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None"""

