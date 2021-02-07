import pygame as pg

clock = pg.time.Clock()
FPS = 30

WIDTH = 800
HEIGHT = 800

pg.init()

running = True
while running:

    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    pg.display.update()
