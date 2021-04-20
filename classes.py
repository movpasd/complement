from pygame import Rect
from warnings import warn


class Node:

    def __init__(self, x, y=None, color=(255, 255, 255)):

        if y is None:
            self.pos = x
        else:
            self.pos = (x, y)

        self.color = color


class Graph:

    def __init__(self):

        self._nodes = []
        self._edges = []

    def get_neighbors(self, node):

        if node not in self._nodes:
            warn("Tried to find neighbors of unavailable node")
            return []

        nbs = []

        for e in self._edges:
            if node == e[0]:
                nbs.append(e[1])
            if node == e[1]:
                nbs.append(e[0])

        return nbs

    def add_node(self, node):

        if node in self._nodes:
            warn("Tried to add already existing node")
        else:
            self._nodes.append(node)

    def remove_node(self, node):

        if node not in self._nodes:
            warn("Tried to remove already existing node")
        else:
            self._nodes.remove(node)

    def get_nodes(self):

        return self._nodes.copy()

    def is_edge(self, node1, node2):

        return ((node1, node2) in self._edges) or ((node2, node1) in self._edges)

    def add_edge(self, node1, node2):

        if self.is_edge(node1, node2):
            warn("Tried to add already existing edge")
        elif node1 == node2:
            warn("Self-edges not supported")
        else:
            self._edges.append((node1, node2))

    def remove_edge(self, node1, node2):

        if (node1, node2) in self._edges:
            self._edges.remove((node1, node2))
        elif (node2, node1) in self._edges:
            self._edges.remove((node2, node1))
        else:
            warn("Tried to remove non-existing edge")

    def flip_edge(self, node1, node2):

        if self.is_edge(node1, node2):
            self.remove_edge(node1, node2)
        else:
            self.add_edge(node1, node2)

    def get_edges(self):

        return self._edges.copy()

    def complement(self, node):

        neighbors = self.get_neighbors(node)
        num = len(neighbors)

        for i in range(num):
            for j in range(i):
                self.flip_edge(neighbors[i], neighbors[j])

    def disconnect(self, node):

        for node2 in self.get_neighbors(node):
            if self.is_edge(node, node2):
                self.remove_edge(node, node2)


class Options:

    def __init__(self, surf, size=30, pad=5, width=3):

        self._mode = "z"

        self.surf = surf
        self.size = size
        self.pad = pad
        self.width = width

        winw, winh = surf.get_size()

        self.rectx = Rect(winw - size - pad, pad, size, size)
        self.recty = Rect(winw - size - pad, size + 2 * pad, size, size)
        self.rectz = Rect(winw - size - pad, 2 * size + 3 * pad, size, size)
        self.rectc = Rect(winw - size - pad, 3 * size + 4 * pad, size, size)

    def get_mode(self):
        return self._mode

    def set_mode(self, i):

        if i == "x" or i == "y" or i == "z" or i == "c":
            self._mode = i
        else:
            warn("Tried to set mode to an unrecognised argument")

    def get_rect(self):

        if self._mode == "x":
            return self.rectx
        elif self._mode == "y":
            return self.recty
        elif self._mode == "z":
            return self.rectz
        elif self._mode == "c":
            return self.rectc
