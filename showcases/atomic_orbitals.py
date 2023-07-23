import yviewer2
from yutility import geometry
import numpy as np

screen = yviewer2.Screen
loop = yviewer2.MainLoop

screen.set_size(1600, 900)
screen.settings.use_3d = True
screen.settings.camera_pos = (0, 0, 6)

# circle
Npoints = 100000
points = np.array([geometry.random_point_on_sphere(3.5) for _ in range(Npoints)]).T
colors = 255 * (np.array([[1, 0, 0]]).T + np.array([[-1, 1, 1]]).T * (points[(0, 0, 0), :]+3.5)/7)

while loop.runs():
    t = loop.state.time/2
    R = geometry.get_rotation_matrix(x=t/1.6, y=t/2.1, z=t/2.6)
    screen.clear()
    screen.draw_pixels(points.T@R, colors)
    screen.update()
