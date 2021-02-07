import pygame as pg
import numpy as np

clock = pg.time.Clock()
FPS = 30

WIDTH = 800
HEIGHT = 800

pg.init()


class Projection:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pg.display.set_mode((width, height))
        self.background = (10, 10, 60)
        pg.display.set_caption('ASCII 3D EARTH')
        self.surfaces = {}

    def addSurface(self, name, surface):
        self.surfaces[name] = surface

    def display(self):
        self.screen.fill(self.background)

        for surface in self.surfaces.values():
            for node in surface.nodes:
                pg.draw.circle(self.screen, (255, 255, 255), (int(node[1]), int(node[2])), 4, 0)

    def rotateAll(self, theta):
        for surface in self.surfaces.values():
            center = surface.findCentre()

            c = np.cos(theta)
            s = np.sin(theta)

            # Rotating about Z - axis
            matrix = np.array([[c, -s, 0, 0],
                               [s, c, 0, 0],
                               [0, 0, 1, 0],
                               [0, 0, 0, 1]])

            surface.rotate(center, matrix)


class Object:
    def __init__(self):
        self.nodes = np.zeros((0, 4))

    def addNodes(self, node_array):
        ones_column = np.ones((len(node_array), 1))
        ones_added = np.hstack((node_array, ones_column))
        self.nodes = np.vstack((self.nodes, ones_added))

    def findCentre(self):
        mean = self.nodes.mean(axis=0)
        return mean

    def rotate(self, center, matrix):
        for i, node in enumerate(self.nodes):
            self.nodes[i] = center + np.matmul(matrix, node - center)


spin = 0

running = True
while running:

    clock.tick(FPS)

    pv = Projection(WIDTH, HEIGHT)

    cube = Object()
    cube_nodes = ([(x, y, z) for x in (200, 600) for y in (200, 600) for z in (200, 600)])
    cube.addNodes(np.array(cube_nodes))
    pv.addSurface('cube', cube)
    pv.rotateAll(spin)
    pv.display()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    pg.display.update()
    spin += 0.05
