import yviewer2
from yutility import geometry
import numpy as np

screen = yviewer2.Screen
loop = yviewer2.MainLoop

screen.set_size(600, 600)

# setup
Nants = 4_000
ant_pos = np.random.rand(Nants, 2) * screen.settings.size
# ant_pos = np.array([screen.middle] * Nants)
# ant_ang = np.random.rand(Nants, 1) * 2 * np.pi
ant_ang = np.linspace(0, 2*np.pi, Nants).reshape(-1, 1)

ant2_pos = np.random.rand(Nants, 2) * screen.settings.size
ant2_ang = np.random.rand(Nants, 1) * 2 * np.pi

# ant_ang = np.zeros((Nants, 1))
pheromones = np.zeros(screen.settings.size)
cols = np.array([(255, 255, 255)] * Nants)
cols2 = np.array([(255, 0, 0)] * Nants)

antenna_length = 20
antenna_angle = 45 * np.pi/180
turning_speed = 2

neighbours = [
    (-1, 1),
    (0, 1),
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, -1),
    (-1, 0),
    ]


while loop.runs():
    screen.clear()

    direc = np.hstack((np.cos(ant_ang), np.sin(ant_ang)))
    ant_pos += direc * 2
    screen.draw_matrix(pheromones/pheromones.max())

    antenna1 = np.mod(ant_pos + np.hstack((np.cos(ant_ang+antenna_angle), np.sin(ant_ang+.4)))*antenna_length, screen.settings.size)
    antenna2 = np.mod(ant_pos + np.hstack((np.cos(ant_ang-antenna_angle), np.sin(ant_ang-.4)))*antenna_length, screen.settings.size)
    antenna1_pheromones = pheromones[antenna1.astype(int)[:, 0], antenna1.astype(int)[:, 1]]
    antenna2_pheromones = pheromones[antenna2.astype(int)[:, 0], antenna2.astype(int)[:, 1]]

    cols = np.array([(255, 255, 255)] * Nants)
    ant_ang += 2*turning_speed*(2*np.random.rand(Nants, 1) - 1) * loop.state.delta_time
    ant_ang[antenna1_pheromones > antenna2_pheromones] += turning_speed * loop.state.delta_time * -1
    ant_ang[antenna1_pheromones < antenna2_pheromones] -= turning_speed * loop.state.delta_time * -1

    ant_pos = np.mod(ant_pos, screen.settings.size)
    pheromones = pheromones * (1 - .1 * loop.state.delta_time)

    pheromones[ant_pos.astype(int)[:, 0], ant_pos.astype(int)[:, 1]] += 1
    screen.draw_pixels(ant_pos, cols)

    # spread pheromones:
    diffuse = np.zeros_like(pheromones)
    for neighbour in neighbours:
        diffuse += np.roll(pheromones, neighbour, (1, 0))/9
    pheromones = diffuse

    if yviewer2.inputs.keys.space:
        pheromones = np.zeros(screen.settings.size)
    # direc = np.hstack((np.cos(ant2_ang), np.sin(ant2_ang)))
    # ant2_pos += direc * loop.state.delta_time * 150

    # antenna1 = np.mod(ant2_pos + np.hstack((np.cos(ant2_ang+antenna_angle), np.sin(ant2_ang+.4)))*antenna_length, screen.settings.size)
    # antenna2 = np.mod(ant2_pos + np.hstack((np.cos(ant2_ang-antenna_angle), np.sin(ant2_ang-.4)))*antenna_length, screen.settings.size)
    # antenna1_pheromones = pheromones[antenna1.astype(int)[:, 0], antenna1.astype(int)[:, 1]]
    # antenna2_pheromones = pheromones[antenna2.astype(int)[:, 0], antenna2.astype(int)[:, 1]]

    # ant2_ang += 4*turning_speed*(2*np.random.rand(Nants, 1) - 1) * loop.state.delta_time
    # ant2_ang[antenna1_pheromones > antenna2_pheromones] -= turning_speed * loop.state.delta_time/2
    # ant2_ang[antenna1_pheromones < antenna2_pheromones] += turning_speed * loop.state.delta_time/2

    # ant2_pos = np.mod(ant2_pos, screen.settings.size)
    # pheromones = pheromones * .99
    # pheromones[ant2_pos.astype(int)[:, 0], ant2_pos.astype(int)[:, 1]] -= 1
    # screen.draw_pixels(ant2_pos, cols2)

    # screen.draw_pixels(ant_pos, cols)
    screen.update()
    print(loop.state.fps)
