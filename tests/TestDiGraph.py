import unittest
from src.DiGraph import DiGraph


class TestDiGraph(unittest.TestCase):

    def setUp(self) -> None:
        self.g = DiGraph()
        self.g.add_node(0)
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

    def tearDown(self) -> None:
        return None

    def test_v_size(self):
        self.assertEqual(7, self.g.v_size())

    def test_e_size(self):
        self.assertEqual(8, self.g.e_size())

    def test_get_all_v(self):
        t = {}
        for node in range(self.g.v_size()):
            t[node] = self.g.nodedict[node]
        self.assertEqual(t, self.g.get_all_v())

    def test_all_in_edges_of_node(self):
        n1 = {3: 1}
        self.assertEqual(n1, self.g.all_in_edges_of_node(1))

    def test_all_out_edges_of_node(self):
        n1 = {2: 3, 3: 2}
        self.assertEqual(n1, self.g.all_out_edges_of_node(1))

    def test_get_mc(self):
        self.assertEqual(15, self.g.get_mc())

    def test_add_edge(self):
        self.assertEqual(True, self.g.add_edge(1, 4, 1.1))
        self.assertEqual(False, self.g.add_edge(1, 4, 1.1))
        self.assertEqual(False, self.g.add_edge(8, 4, 1.1))

    def test_add_node(self):
        self.assertEqual(True, self.g.add_node(8))
        self.assertEqual(False, self.g.add_node(8))

    def test_remove_node(self):
        self.assertEqual(True, self.g.remove_node(1))
        self.assertEqual(False, self.g.remove_node(1))

    def test_remove_edge(self):
        self.assertEqual(True, self.g.remove_edge(1, 2))
        self.assertEqual(False, self.g.remove_edge(1, 2))


if __name__ == '__main__':
    unittest.main()
