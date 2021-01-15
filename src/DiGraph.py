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
    """
           Returns the number of vertices in this graph
           @return: The number of vertices in this graph
           """

    def e_size(self) -> int:
        c = 0
        for src, edge in self.edgedict.items():
            c += len(edge)
        return c
    """
          Returns the number of edges in this graph
          @return: The number of edges in this graph
          """

    def get_all_v(self) -> dict:
        return self.nodedict
    """return a dictionary of all the nodes in the Graph, each node is represented using a pair
            (node_id, node_data)
           """

    def all_in_edges_of_node(self, id1: int) -> dict:
        ans = {}
        if id1 not in self.nodedict or self is None:
            return ans
        for key in self.edgedict:
            if key != id1:
                if id1 in self.edgedict[key].keys():
                    ans[key] = self.edgedict[key][id1]
        return ans
    """return a dictionary of all the nodes connected to (into) node_id ,
          each node is represented using a pair (other_node_id, weight)
           """

    def all_out_edges_of_node(self, id1: int) -> dict:
        return self.edgedict[id1]
    """return a dictionary of all the nodes connected from node_id , each node is represented using a pair
           (other_node_id, weight)
           """

    def get_mc(self) -> int:
        return self.mc
    """
           Returns the current version of this graph,
           on every change in the graph state - the MC should be increased
           @return: The current version of this graph.
           """

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
        """
               Adds an edge to the graph.
               @param id1: The start node of the edge
               @param id2: The end node of the edge
               @param weight: The weight of the edge
               @return: True if the edge was added successfully, False o.w.

               Note: If the edge already exists or one of the nodes dose not exists the functions will do nothing
               """

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if node_id not in self.nodedict:
            if pos is None:
                pos = (random.random() * 40, random.random() * 40, 0.0)
            n = Node(node_id, pos)
            self.nodedict[node_id] = n
            self.mc += 1
            return True
        return False
    """
           Adds a node to the graph.
           @param node_id: The node ID
           @param pos: The position of the node
           @return: True if the node was added successfully, False o.w.

           Note: if the node id already exists the node will not be added
           """

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
    """
          Removes a node from the graph.
          @param node_id: The node ID
          @return: True if the node was removed successfully, False o.w.

          Note: if the node id does not exists the function will do nothing
          """

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if node_id1 != node_id2 and node_id1 in self.nodedict and node_id2 in self.nodedict and node_id2 in \
                self.edgedict[node_id1]:
            del self.edgedict[node_id1][node_id2]
            self.mc += 1
            return True
        return False
    """Removes an edge from the graph.
        @param node_id1: The start node of the edge
        @param node_id2: The end node of the edge
        @return: True if the edge was removed successfully, False o.w.

        Note: If such an edge does not exists the function will do nothing"""

