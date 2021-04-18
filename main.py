import pygame
from warnings import warn
from collections import namedtuple

NODE_SIZE = 10
LINE_WIDTH = 3

COLOR_BG = (150, 150, 150)
COLOR_NODE = (255, 255, 255)
COLOR_LINE = (255, 255, 255)

WIN_SIZE = (800, 800)
WIN_MIDDLE = (400, 400)
WIN_SCALE = 50


def pixels(pos):

    if (type(pos) is tuple) and (len(pos) == 2):

        return (int(WIN_MIDDLE[0] + WIN_SCALE * pos[0]),
                int(WIN_MIDDLE[1] - WIN_SCALE * pos[1]))

    elif (type(pos) is float) or (type(pos) is int):

        return int(WIN_SCALE) * pos

    else:

        warn("Invalid argument for pixels")


def realpos(pixels):

    if type(pixels) is tuple and len(pixels) == 2:

        return ((pixels[0] - WIN_MIDDLE[0]) / WIN_SCALE,
                (pixels[1] + WIN_MIDDLE[1]) / WIN_SCALE)

    elif type(pixels) is float or type(pixels) is int:

        return pixels / WIN_SCALE

    else:

        warn("Invalid arguemnt for realpos")


def draw_node(surf, pos):

    pygame.draw.circle(surf, COLOR_NODE, pixels(pos), NODE_SIZE)


def draw_line(surf, pos1, pos2):

    pygame.draw.line(surf, COLOR_LINE, pixels(pos1), pixels(pos2), LINE_WIDTH)


def draw_graph(surf, graph):

    for node in graph.get_nodes():

        draw_node(surf, node.pos)

    for edge in graph.get_edges():
        draw_line(surf, edge[0].pos, edge[1].pos)


# =====


class Node:

    def __init__(self, x, y=None):

        if y is None:
            self.pos = x
        else:
            self.pos = (x, y)


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

    def apply_complement(self, node):

        neighbors = self.get_neighbors(node)
        num = len(neighbors)

        for i in range(num):
            for j in range(i):
                self.flip_edge(neighbors[i], neighbors[j])


def grid_graph(width, height, spacing=1, centering=(0, 0)):

    graph = Graph()

    left = centering[0] - (width - 1) * spacing / 2
    bottom = centering[1] - (height - 1) * spacing / 2

    nodes = []

    for i in range(width):

        col = []

        for j in range(height):

            node = Node((left + spacing * i, bottom + spacing * j))
            col.append(node)
            graph.add_node(node)

        nodes.append(col)

    for i in range(width - 1):
        for j in range(height):
            graph.add_edge(nodes[i][j], nodes[i + 1][j])

    for j in range(height - 1):
        for i in range(width):
            graph.add_edge(nodes[i][j], nodes[i][j + 1])

    return graph


Game = namedtuple("Game", ["graph"])


def init():

    pygame.init()
    screen = pygame.display.set_mode(WIN_SIZE)
    screen.fill(COLOR_BG)
    pygame.display.update()

    graph = grid_graph(3, 3, 3)

    game = Game(graph)

    return screen, game


def update(screen, game):

    screen.fill(COLOR_BG)

    draw_graph(screen, game.graph)

    pygame.display.update()


if __name__ == "__main__":

    screen, game = init()

    running = True

    while running:

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:

                running = False

            elif ev.type == pygame.MOUSEBUTTONUP:

                if ev.button == 1:
                    for n in game.graph.get_nodes():
                        npos = pixels(n.pos)
                        if (npos[0] - ev.pos[0])**2 + (npos[1] - ev.pos[1])**2 <= NODE_SIZE**2:
                            game.graph.apply_complement(n)

        update(screen, game)

    pygame.quit()
