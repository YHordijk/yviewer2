import pygame as pg
from yutility import dictfunc, geometry
import numpy as np


class Screen:
    def __init__(self):
        self.state = dictfunc.DotDict({
        })
        self.settings = dictfunc.DotDict({
            'size': (400, 400),
            'use_3d': False,
            'mode_3d': 'perspective',
            'camera_pos': (0, 0, 0),
            'camera_rot': (0, 0, 0),
            'camera_plane_pos': (200, 200, 600),
            'background_color': (0, 0, 0),
        })
        self.initialize()

    def initialize(self):
        self.draw_surf = pg.display.set_mode(self.settings.size)

    def set_size(self, width, height):
        self.settings.size = (width, height)
        self.settings.camera_plane_pos = (width/2, height/2, 600)
        self.initialize()

    def draw_pixels(self, poss, colors=None):
        poss = self.project(poss).astype(int)
        colors = colors if colors is not None else [(255, 255, 255)] * len(poss)
        # for pos, color in zip(poss, colors):
        #     print(pos)
        #     self.draw_surf.set_at([int(pos[0]), int(pos[1])], color)
        pixels = pg.surfarray.pixels3d(self.draw_surf)
        pixels[poss[:,0], poss[:,1], :] = colors.T
        del pixels


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

    def project(self, poss):
        poss = np.atleast_2d(poss)

        if not self.settings.use_3d:
            return poss

        if self.settings.mode_3d == 'perspective':
            R = geometry.get_rotation_matrix(*self.settings.camera_rot).T
            x = poss - self.settings.camera_pos

            # print(x.shape, R.shape)
            d = R @ x.T
            e = self.settings.camera_plane_pos
            P = np.array([[1, 0, e[0] / e[2]], [0, 1, e[1] / e[2]], [0, 0, 1 / e[2]]])

            f = P @ d
            return np.vstack((f[0] / f[2], f[1] / f[2])).T



