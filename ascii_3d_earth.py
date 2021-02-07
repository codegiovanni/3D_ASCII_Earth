import pygame as pg
import numpy as np
from math import pi, sin, cos

clock = pg.time.Clock()
FPS = 30

WIDTH = 1920
HEIGHT = 1080

R = 350
MAP_WIDTH = 139
MAP_HEIGHT = 34

pg.init()

my_font = pg.font.SysFont('arial', 18)

with open('earth_W140_H35.txt', 'r') as file:
    data = [file.read().replace('\n', '')]

    print(data)

ascii_chars = []
for line in data:
    for char in line:
        ascii_chars.append(char)

inverted_ascii_chars = ascii_chars[::-1]


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
            i = 0
            for node in surface.nodes:
                self.text = inverted_ascii_chars[i]
                self.text_surface = my_font.render(self.text, False, (0, 255, 0))
                if i > MAP_WIDTH - 1 and i < (MAP_WIDTH * MAP_HEIGHT - MAP_WIDTH) and node[1] > 0:
                    self.screen.blit(self.text_surface, (WIDTH / 2 + int(node[0]), HEIGHT / 2 + int(node[2])))
                i += 1

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
    spin += 0.05
