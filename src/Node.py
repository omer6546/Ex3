import sys


class Node:
    def __init__(self, key, pos):
        self.key = key
        self.weight = sys.float_info.max
        self.info = " "
        self.tag = 0
        if pos is None:
            self.pos = self.Geolocation()
        else:
            self.pos = pos

    class Geolocation:
        def __init__(self, x=0, y=0, z=0):
            self.loc = (x, y, z)

        def __repr__(self):
            return "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"

    def __lt__(self, other):
        return self.weight < other.weight

    def __str__(self):
        return "key: " + str(self.key) + "pos: " + str(self.pos)

    def get_key(self):
        return self.key

    def set_weight(self, weight):
        self.weight = weight

    def get_weight(self) -> float:
        return self.weight

    def set_info(self, info):
        self.info = info

    def get_info(self) -> str:
        return self.info

    def set_tag(self, tag):
        self.tag = tag

    def get_tag(self) -> int:
        return self.tag

    def set_pos(self, x, y, z):
        self.pos = (x, y, z)

    def get_pos(self) -> Geolocation:
        return self.pos
