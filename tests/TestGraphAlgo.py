import unittest

from numpy import inf

from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo


class TestGraphAlgo(unittest.TestCase):

    def setUp(self) -> None:
        self.g = DiGraph()
        self.g.add_node(1)
        self.g.add_node(2)
        self.g.add_node(3)
        self.g.add_node(4)
        self.g.add_node(5)
        self.g.add_node(6)
        self.g.add_edge(1, 2, 3)
        self.g.add_edge(1, 3, 2)
        self.g.add_edge(2, 5, 3)
        self.g.add_edge(3, 1, 1)
        self.g.add_edge(3, 4, 2)
        self.g.add_edge(4, 3, 1)
        self.g.add_edge(4, 5, 1)
        self.g.add_edge(6, 2, 1)
        self.ga = GraphAlgo(self.g)

    def tearDown(self) -> None:
        return None

    def test_get_graph(self):
        self.ga.save_to_json('testgraph.json')
        self.assertEqual(self.g, self.ga.get_graph())

    def test_load_save_json(self):
        self.assertEqual(self.g, self.ga.get_graph())

    def test_shortest_path(self):
        self.assertEqual((5, [1, 3, 4, 5]), self.ga.shortest_path(1, 5))
        self.assertEqual((inf, []), self.ga.shortest_path(1, 7))
        self.assertEqual((inf, []), self.ga.shortest_path(1, 6))

    def test_connected_component(self):
        self.assertEqual([1, 3, 4], self.ga.connected_component(1))
        self.ga.get_graph().remove_node(1)
        self.assertEqual([], self.ga.connected_component(1))
        self.ga = GraphAlgo(None)
        self.assertEqual([], self.ga.connected_component(1))

    def test_connected_components(self):
        self.assertEqual([[1, 3, 4], [2], [5], [6]], self.ga.connected_components())
        self.ga = GraphAlgo(None)
        self.assertEqual([], self.ga.connected_components())


if __name__ == '__main__':
    unittest.main()
