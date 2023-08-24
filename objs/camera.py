import numpy as np
import inputs, screen



class OrbitCamera3D:
	def __init__(self, target=None):
		self.target = target or np.array((0, 0, 0))
		self.rotation = np.array([0, 0])
		self.distance_offset = np.array([0, 0, 0])

	def update(self):
		
