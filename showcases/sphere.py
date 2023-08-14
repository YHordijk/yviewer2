import yviewer2
from yutility import geometry
import numpy as np
from math import factorial, pi, sqrt

screen = yviewer2.Screen
loop = yviewer2.MainLoop

screen.set_size(1600, 900)
screen.settings.use_3d = True
screen.settings.camera_pos = [0, 0, 6]

# 2p orbital
xi = 3


class STO:
    def __init__(self, n=1, l=0, ml=0):
        self.n = n
        self.l = l
        self.ml = ml

        self.validate()

    def __repr__(self):
        return f'STO(n={self.n}, l={self.l}, ml={self.ml})'

    def __str__(self):
        return self.name

    def validate(self):
        assert self.n > 0, 'Principle quantum number must be n >= 1'
        assert self.l in range(self.n+1), f'Angular momentum quantum number must be 0 <= l <= {self.n}'
        assert self.ml in range(-self.l, self.l+1), f'Magnetic quantum number must be -{self.l} <= ml <m {self.l}'

    @property
    def name(self):
        angular = ['s', 'p', 'd', 'f', 'g', 'h'][self.l]
        magnetic = ''
        if angular == 'p':
            magnetic = ['y', 'z', 'x'][self.ml + self.l]
        elif angular == 'd':
            magnetic = ['xy', 'yz', 'z2', 'xz', 'xx-yy'][self.ml + self.l]
        elif angular == 'f':
            magnetic = ['y(3xx-yy)', 'xyz', 'yzz', 'zzz', 'xzz', 'z(xx-yy)', 'x(xx-3yy)'][self.ml + self.l]    
        return f'{self.n}{angular}{magnetic}'

    def __call__(self, coords):
        return self.radial(coords) * self.spherical(coords)

    def radial(self, coords):
        r = np.linalg.norm(coords, axis=1)
        x, y, z = coords[:, 0], coords[:, 1], coords[:, 2]
        # return r**(self.n-1)*np.exp(-xi*r) * (2*xi)**self.n * np.sqrt(2*xi/(factorial(2*self.n)))
        # if self.l == 0:
        return sqrt(1/pi)*np.exp(-r)

        # if self.l == 1:
        #     if self.ml == -1:
        #         return sqrt(3/(4*pi)) * y/r
        #     if self.ml == 0:
        #         return sqrt(3/(4*pi)) * z/r
        #     if self.ml == 1:
        #         return sqrt(3/(4*pi)) * x/r

        # if self.l == 2:
        #     if self.ml == -2:
        #         return sqrt(15/pi)/2 * x*y/r**2
        #     if self.ml == -1:
        #         return sqrt(15/pi)/2 * y*z/r**2
        #     if self.ml == 0:
        #         return sqrt(5/pi)/4 * (3*z**2/r**2 - 1)
        #     if self.ml == 1:
        #         return sqrt(15/pi)/2 * x*z/r**2
        #     if self.ml == 2:
        #         return sqrt(15/pi)/4 * (x**2 - y**2)/r**2

        # if self.l == 3:
        #     if self.ml == -3:
        #         return sqrt(35/2/pi)/4 * y/3**3 * (3*x**2-y**2)
        #     if self.ml == -2:
        #         return sqrt(105/pi)/2 * x*y*z/r**3
        #     if self.ml == -1:
        #         return sqrt(10.5/pi)/4 * y/r**3 * (5*z**2 - r**2)
        #     if self.ml == 0:
        #         return sqrt(7/pi)/4 * (5*z**3 - 3*z*r**2)/r**3
        #     if self.ml == 1:
        #         return sqrt(10.5/pi)/4 * x/r**3 * (5*z**2 - r**2)
        #     if self.ml == 2:
        #         return sqrt(105/pi)/4 * z*(x**2 - y**2)/r**3
        #     if self.ml == 3:
        #         return sqrt(17.5/pi)/4 * x*(x**2 - 3*y**2)/r**3

        # if self.l == 4:
        #     if self.ml == -4:
        #         return .75 * sqrt(35/pi) * x*y*(x**2-y**2)/r**4
        #     if self.ml == -3:
        #         return .75 * sqrt(17.5/pi) * z*y*(3*x**2-y**2)/r**4
        #     if self.ml == -2:
        #         return .75 * sqrt(5/pi) * x*y*(7*z**2-r**2)/r**4
        #     if self.ml == -1:
        #         return .75 * sqrt(2.5/pi) * y*(7*z**3-z*r**2)/r**4
        #     if self.ml == 0:
        #         return 3/16*sqrt(1/pi) * (35*z**2*r**2 - 30*z**2*r**2 + 3*r**4)/r**4
        #     if self.ml == 1:
        #         return .75 * sqrt(2.5/pi) * x/r**4 * (7*z**3 - 3*z*r**2)
        #     if self.ml == 2:
        #         return 3/8 * sqrt(5/pi) * (x**2 - y**2) * (7*z**2 - r**2)/r**4
        #     if self.ml == 3:
        #         return .75 * sqrt(35/pi/2) * x*(x**2 - 3*y**2) * z / r**4
        #     if self.ml == 4:
        #         return 3/16 * sqrt(35/pi) * (x**2 * (x**2 - 3*y**2) - y**2 * (3*x**2 - y**2))/r**4


    def spherical(self, coords):
        r = np.linalg.norm(coords, axis=1)
        x, y, z = coords[:, 0], coords[:, 1], coords[:, 2]
        if self.l == 0:
            return sqrt(1/pi)/2

        if self.l == 1:
            if self.ml == -1:
                return sqrt(3/(4*pi)) * y/r
            if self.ml == 0:
                return sqrt(3/(4*pi)) * z/r
            if self.ml == 1:
                return sqrt(3/(4*pi)) * x/r

        if self.l == 2:
            if self.ml == -2:
                return sqrt(15/pi)/2 * x*y/r**2
            if self.ml == -1:
                return sqrt(15/pi)/2 * y*z/r**2
            if self.ml == 0:
                return sqrt(5/pi)/4 * (3*z**2/r**2 - 1)
            if self.ml == 1:
                return sqrt(15/pi)/2 * x*z/r**2
            if self.ml == 2:
                return sqrt(15/pi)/4 * (x**2 - y**2)/r**2

        if self.l == 3:
            if self.ml == -3:
                return sqrt(35/2/pi)/4 * y/3**3 * (3*x**2-y**2)
            if self.ml == -2:
                return sqrt(105/pi)/2 * x*y*z/r**3
            if self.ml == -1:
                return sqrt(10.5/pi)/4 * y/r**3 * (5*z**2 - r**2)
            if self.ml == 0:
                return sqrt(7/pi)/4 * (5*z**3 - 3*z*r**2)/r**3
            if self.ml == 1:
                return sqrt(10.5/pi)/4 * x/r**3 * (5*z**2 - r**2)
            if self.ml == 2:
                return sqrt(105/pi)/4 * z*(x**2 - y**2)/r**3
            if self.ml == 3:
                return sqrt(17.5/pi)/4 * x*(x**2 - 3*y**2)/r**3

        if self.l == 4:
            if self.ml == -4:
                return .75 * sqrt(35/pi) * x*y*(x**2-y**2)/r**4
            if self.ml == -3:
                return .75 * sqrt(17.5/pi) * z*y*(3*x**2-y**2)/r**4
            if self.ml == -2:
                return .75 * sqrt(5/pi) * x*y*(7*z**2-r**2)/r**4
            if self.ml == -1:
                return .75 * sqrt(2.5/pi) * y*(7*z**3-z*r**2)/r**4
            if self.ml == 0:
                return 3/16*sqrt(1/pi) * (35*z**2*r**2 - 30*z**2*r**2 + 3*r**4)/r**4
            if self.ml == 1:
                return .75 * sqrt(2.5/pi) * x/r**4 * (7*z**3 - 3*z*r**2)
            if self.ml == 2:
                return 3/8 * sqrt(5/pi) * (x**2 - y**2) * (7*z**2 - r**2)/r**4
            if self.ml == 3:
                return .75 * sqrt(35/pi/2) * x*(x**2 - 3*y**2) * z / r**4
            if self.ml == 4:
                return 3/16 * sqrt(35/pi) * (x**2 * (x**2 - 3*y**2) - y**2 * (3*x**2 - y**2))/r**4


orb = STO(n=3, l=3, ml=-2)

rot = (0, 0)
rotation = (0, 0)
zoom = 0
while loop.runs():
    t = loop.state.time/2

    points = geometry.random_point_on_sphere(5, N=50_000)
    wfs = orb(points).reshape(-1, 1)
    RED = np.array([255, 0, 0])
    BLUE = np.array([255, 255, 255])
    colors = np.where(wfs > 0, RED, BLUE)
    colors = colors * abs(wfs)/abs(wfs).max()

    rot = (rot[0]*.95, rot[1]*.95)
    rotation = rotation[0] + rot[0], rotation[1] + rot[1]
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
    R = geometry.get_rotation_matrix(x=rotation[0], y=rotation[1])
    points = points @ R

    # idxs = np.argsort(screen.distance_to_camera(points))
    # screen.draw_pixels(points[idxs], colors[idxs].T)
    # screen.draw_circles(points, 1, colors=colors)

    screen.draw_pixels(points, colors.T)
    screen.draw_axes()
    screen.update()
