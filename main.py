import pygame
from pygame import Rect
from warnings import warn
from collections import namedtuple

import random

from classes import Node, Graph, Options


pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont(None, 24)


NODE_SIZE = 10
LINE_WIDTH = 3

JIGGLE = 0.1

CWHITE = (255, 255, 255)
CBLACK = (0, 0, 0)
CRED = (255, 0, 0)
CYELLOW = (255, 255, 0)
CGREEN = (0, 255, 0)
CCYAN = (0, 255, 255)
CBLUE = (0, 0, 255)
CMAGENTA = (255, 0, 255)

COLOR_BG = (150, 150, 150)
COLOR_LINE = CWHITE

WIN_SIZE = (800, 800)
WIN_MIDDLE = (400, 400)
WIN_SCALE = 50

GRID_WIDTH = 5
GRID_HEIGHT = 3
GRID_SPACING = 1


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


def draw_node(surf, node):

    pygame.draw.circle(surf, node.color, pixels(node.pos), NODE_SIZE)


def draw_line(surf, pos1, pos2):

    pygame.draw.line(surf, COLOR_LINE, pixels(pos1), pixels(pos2), LINE_WIDTH)


def draw_graph(surf, graph):

    for node in graph.get_nodes():

        draw_node(surf, node)

    for edge in graph.get_edges():
        draw_line(surf, edge[0].pos, edge[1].pos)


def draw_options(surf, opt):

    winw, winh = surf.get_size()

    # Draw the squares for the three options
    pygame.draw.rect(surf, CRED, opt.rectx)
    surf.blit(FONT.render("X", True, CBLACK), opt.rectx.move(opt.pad, opt.pad))

    pygame.draw.rect(surf, CGREEN, opt.recty)
    surf.blit(FONT.render("Y", True, CBLACK), opt.recty.move(opt.pad, opt.pad))

    pygame.draw.rect(surf, CBLUE, opt.rectz)
    surf.blit(FONT.render("Z", True, CBLACK), opt.rectz.move(opt.pad, opt.pad))

    pygame.draw.rect(surf, CWHITE, opt.rectc)
    surf.blit(FONT.render("LC", True, CBLACK),
              opt.rectc.move(opt.pad, opt.pad))

    # Draw the gold square around current option
    pygame.draw.rect(surf, CYELLOW, opt.get_rect(), width=opt.width)


# =====


def rand():
    return random.random()


def grid_graph(width, height, spacing=1, centering=(0, 0), jiggle=0):

    graph = Graph()

    left = centering[0] - (width - 1) * spacing / 2
    bottom = centering[1] - (height - 1) * spacing / 2

    nodes = []

    for i in range(width):

        col = []

        for j in range(height):

            jigx = jiggle * rand()
            jigy = jiggle * rand()

            node = Node((left + spacing * i + jigx,
                         bottom + spacing * j + jigy))
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


def apply_rule(node, graph, mode):

    if mode == "x":

        nbs = graph.get_neighbors(node)

        if len(nbs) > 0:
            bnode = random.choice(nbs)
            graph.complement(bnode)
            graph.complement(node)
            graph.disconnect(node)
            graph.complement(bnode)

        node.color = CBLACK

    elif mode == "y":

        graph.complement(node)
        graph.disconnect(node)
        node.color = CBLACK

    elif mode == "z":

        graph.disconnect(node)
        node.color = CBLACK

    elif mode == "c":

        graph.complement(node)

Game = namedtuple("Game", ["graph", "options"])


def init():

    screen = pygame.display.set_mode(WIN_SIZE)
    screen.fill(COLOR_BG)
    pygame.display.update()

    game = new_game(screen)

    return screen, game


def new_game(screen):

    graph = grid_graph(GRID_WIDTH, GRID_HEIGHT, GRID_SPACING, jiggle=JIGGLE)
    options = Options(screen)

    game = Game(graph, options)

    return game


def update(screen, game):

    screen.fill(COLOR_BG)

    draw_graph(screen, game.graph)
    draw_options(screen, game.options)

    pygame.display.update()


if __name__ == "__main__":

    screen, game = init()

    running = True

    while running:

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:

                running = False

            elif ev.type == pygame.MOUSEBUTTONUP:

                # LEFT MOUSE BUTTON
                if ev.button == 1:

                    rx, ry, rz, rc = (game.options.rectx,
                                      game.options.recty,
                                      game.options.rectz,
                                      game.options.rectc)

                    if rx.collidepoint(ev.pos):
                        game.options.set_mode("x")
                    if ry.collidepoint(ev.pos):
                        game.options.set_mode("y")
                    if rz.collidepoint(ev.pos):
                        game.options.set_mode("z")
                    if rc.collidepoint(ev.pos):
                        game.options.set_mode("c")

                    for n in game.graph.get_nodes():
                        npos = pixels(n.pos)
                        if (npos[0] - ev.pos[0])**2 + (npos[1] - ev.pos[1])**2 <= NODE_SIZE**2:
                            apply_rule(n, game.graph, game.options.get_mode())

                # RIGHT MOUSE BUTTON
                if ev.button == 3:
                    pass

            elif ev.type == pygame.KEYDOWN:

                if ev.key == pygame.K_r:
                    game = new_game(screen)

        update(screen, game)

    pygame.quit()
