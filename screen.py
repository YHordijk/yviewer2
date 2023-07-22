import pygame as pg
from yutility import dictfunc


class Screen:
    def __init__(self):
        self.state = dictfunc.DotDict({
        })
        self.settings = dictfunc.DotDict({
            'size': (400, 400),
            'use_3d': False,
            'background_color': (0, 0, 0),
        })
        self.initialize()

    def initialize(self):
        self.draw_surf = pg.display.set_mode(self.settings.size)

    def draw_pixels(self, poss, colors):
        for pos, color in zip(poss, colors):
            self.draw_surf.set_at([int(pos[0]), int(pos[1])], color)

    def clear(self, color=None):
        color = color or self.settings.background_color
        self.draw_surf.fill(color)

    def update(self):
        pg.display.flip()

    @property
    def middle(self):
        return self.settings.size[0]/2, self.settings.size[1]/2

    @property
    def middle_x(self):
        return self.settings.size[0]/2

    @property
    def middle_y(self):
        return self.settings.size[1]/2
