import pygame as pg
from yutility import dictfunc, geometry, ensure_list
import numpy as np
import itertools
import cv2
from skimage import draw


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
            'space_type_2d': 'pixel',
            'extent_min_2d': (0, 1),
            'extent_max_2d': (0, 1),
        })
        self.initialize()

    def initialize(self):
        self.draw_surf = pg.display.set_mode(self.settings.size)

    def set_size(self, width, height):
        self.settings.size = (width, height)
        self.settings.camera_plane_pos = (width/2, height/2, 600)
        self.initialize()

    def draw_matrix(self, matrix, color=[255, 255, 255]):
        pixels = pg.surfarray.pixels3d(self.draw_surf)
        pixels[:, :, 0] = color[0] * matrix
        pixels[:, :, 1] = color[1] * matrix
        pixels[:, :, 2] = color[2] * matrix
        del pixels

    def draw_pixels(self, poss, colors=None, pixel_offsets=None):
        poss = self.project(poss).astype(int)
        colors = colors if colors is not None else np.array([(255, 255, 255)] * len(poss))

        pixel_offsets = pixel_offsets or [(0, 0)]

        pixels = pg.surfarray.pixels3d(self.draw_surf)
        for (offsetx, offsety) in pixel_offsets:
            pixels[np.clip(poss[:, 0]+offsetx, 0, self.settings.size[0]-1), np.clip(poss[:, 1]+offsety, 0, self.settings.size[1]-1), :] = colors

        del pixels

    def draw_circles(self, poss, radii=1, colors=None, filled=True):
        poss_proj = self.project(poss).astype(int)
        colors = colors if colors is not None else np.array([(255, 255, 255)] * len(poss)).T
        pixels = pg.surfarray.pixels3d(self.draw_surf)

        radii = ensure_list(radii)
        if len(radii) == 1:
            radii = radii * len(poss)

        radii = self.project(np.array(poss) + np.vstack([np.zeros_like(radii), np.zeros_like(radii), np.array(radii)]).T) - poss_proj
        radii = np.linalg.norm(radii, axis=1)

        if filled:
            for pos, color, radius in zip(poss_proj, colors, radii):
                # rr, cc = draw.disk((radius, radius), radius=radius, shape=(radius*2, radius*2))
                # pixels[rr + pos[0], cc + pos[1]] = color
                rr, cc = draw.circle(*pos, radius=radius, shape=pixels.shape)
                pixels[rr, cc] = color
        else:
            for pos, color, radius in zip(poss_proj, colors, radii):
                rr, cc, val = draw.circle_perimeter_aa(*pos, radius=radius, shape=pixels.shape)
                pixels[rr, cc] = color * val.reshape(-1, 1)

        del pixels

    def draw_line(self, start, end, color=None, width=1):
        color = color if color is not None else (255, 255, 255)
        start_ = self.project(start).astype(int)
        end_ = self.project(end).astype(int)
        pg.draw.line(self.draw_surf, color, start_, end_, width=width)

    def draw_axes(self, length=1):
        self.draw_line([0, 0, 0], [1, 0, 0], [255, 0, 0])
        self.draw_line([0, 0, 0], [0, 1, 0], [0, 255, 0])
        self.draw_line([0, 0, 0], [0, 0, 1], [0, 0, 255])

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
            if self.settings.space_type_2d == 'pixel':
                return poss
            elif self.settings.space_type_2d == 'extent':
                return (poss - np.array(self.settings.extent_min_2d)) / (np.array(self.settings.extent_max_2d) - np.array(self.settings.extent_min_2d))

        if self.settings.mode_3d == 'perspective':
            R = geometry.get_rotation_matrix(*self.settings.camera_rot).T
            x = poss - self.settings.camera_pos

            d = R @ x.T
            e = self.settings.camera_plane_pos
            P = np.array([[1, 0, e[0] / e[2]], [0, 1, e[1] / e[2]], [0, 0, 1 / e[2]]])

            f = P @ d
            return np.squeeze(np.vstack((f[0] / f[2], f[1] / f[2])).T)

    def distance_to_camera(self, poss):
        return np.linalg.norm(poss - self.settings.camera_pos, axis=1)
