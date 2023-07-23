from yutility import dictfunc
from yviewer2 import inputs
import pygame as pg


class MainLoop:
    def __init__(self):
        self.state = dictfunc.DotDict({
            'iteration': 0,
            'time': 0,
            'delta_time': 0,
            'fps': 0,
        })
        self.settings = dictfunc.DotDict({
            'fps': 60
        })
        self.clock = pg.time.Clock()

    def should_exit(self):
        if inputs.keys.escape:
            return True
        if pg.event.peek(pg.QUIT):
            return True
        if self.state.should_exit_flag:
            return True

    def runs(self):
        inputs.update()
        self.state.iteration += 1
        dt = self.clock.tick_busy_loop(self.settings.fps) / 1000
        self.state.delta_time = dt
        self.state.time += dt
        self.state.fps = 1/dt

        return not self.should_exit()

    def stop(self, now=False):
        self.state.should_exit_flag = True


