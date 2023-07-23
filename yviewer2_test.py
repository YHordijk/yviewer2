import yviewer2
from yutility import geometry
import numpy as np
from math import factorial

screen = yviewer2.Screen
loop = yviewer2.MainLoop

screen.set_size(1600, 900)
screen.settings.use_3d = True
screen.settings.camera_pos = (0, 0, 6)

# # circle
# Npoints = 200000
# points = np.array([geometry.random_point_in_sphere(3) for _ in range(Npoints)]).T
# while loop.runs():
# 	t = loop.state.time/2
# 	R = geometry.get_rotation_matrix(x=t/1.6, y=t/2.1, z=t/2.6)
# 	screen.clear()
# 	colors = 255 * (np.array([[1, 0, 0]]).T + np.array([[-1, 1, 0]]).T * (points[(0,0,1),:]+3)/6)
# 	screen.draw_pixels(points.T@R, colors)
# 	screen.update()


# 2p orbital
xi = 4
def slater(coords, n):
	r = np.linalg.norm(coords, axis=1)
	return r**n*np.exp(-xi*r) * (2*xi)**n * np.sqrt(2*xi/(factorial(2*n))) * (coords[:, 0]**2 + coords[:, 1]**2)

points = []
wfs = []
while len(points) < 100000:
	p = geometry.random_point_in_sphere(3)
	wf = slater(np.array([p]), n=4)
	# if abs(wf) > np.random.rand():
	points.append(p)
	wfs.append(wf)

points = np.array(points)
wfs = np.array(wfs)
colors = np.where(wfs > 0, (255, 0, 0), (0, 0, 255))
colors = colors * abs(wfs)/abs(wfs).max()

while loop.runs():
	t = loop.state.time/2
	R = geometry.get_rotation_matrix(x=t/1.6, y=t/2.1, z=t/2.6)
	screen.clear()
	screen.draw_pixels(points@R, colors.T)
	screen.update()
