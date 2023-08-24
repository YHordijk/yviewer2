import yviewer2
from yutility import geometry
import numpy as np

screen = yviewer2.Screen
loop = yviewer2.MainLoop

screen.set_size(1600, 900)
screen.settings.use_3d = True
screen.settings.camera_pos = [0, 0, 6]

points = np.array([[1, 1, 1], [1, 1, -1], 
				   [1, -1, 1], [1, -1, -1],
				   [-1, 1, 1], [-1, 1, -1],
				   [-1, -1, 1], [-1, -1, -1]])

colors = [[205, 205, 205]] * (points + 1)/2 + 50

rot = (0, 0)
zoom = 0
while loop.runs():
    t = loop.state.time/2

    rot = (rot[0]*.95, rot[1]*.95)
    zoom = zoom*.75
    if yviewer2.inputs.mouse.left.hold:
        screen.clear()
        rot = (-yviewer2.inputs.mouse.dy/600, yviewer2.inputs.mouse.dx/600)
    if yviewer2.inputs.mouse.scrollup:
        screen.clear()
        zoom = -.25
    if yviewer2.inputs.mouse.scrolldown:
        screen.clear()
        zoom = .25

    screen.settings.camera_pos[2] += zoom
    R = geometry.get_rotation_matrix(x=rot[0], y=rot[1])
    points = points @ R

    screen.clear()
    screen.draw_circles(points @ R, .5, colors, filled=False)
    screen.update()
