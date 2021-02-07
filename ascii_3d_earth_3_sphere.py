import pygame as pg
import numpy as np
from math import pi, sin, cos

clock = pg.time.Clock()
FPS = 30

WIDTH = 800
HEIGHT = 800

R = 250
MAP_WIDTH = 40
MAP_HEIGHT = 20

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
                pg.draw.circle(self.screen, (255, 255, 255), (WIDTH / 2 + int(node[1]), HEIGHT / 2 + int(node[2])), 2,
                               0)

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


xyz = []

for i in range(MAP_HEIGHT + 1):
    lat = (pi / MAP_HEIGHT) * i
    for j in range(MAP_WIDTH + 1):
        lon = (2 * pi / MAP_WIDTH) * j
        x = round(R * sin(lat) * cos(lon), 2)
        y = round(R * sin(lat) * sin(lon), 2)
        z = round(R * cos(lat), 2)
        xyz.append((x, y, z))

spin = 0

for i in range(5):
    print(i)

running = True
while running:

    clock.tick(FPS)

    pv = Projection(WIDTH, HEIGHT)

    globe = Object()
    globe_nodes = [i for i in xyz]
    globe.addNodes(np.array(globe_nodes))
    pv.addSurface('globe', globe)
    pv.rotateAll(spin)
    pv.display()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    pg.display.update()
    # spin += 0.05
