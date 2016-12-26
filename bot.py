import numpy as np

SONIC_MAX_DISTANCE = 5.0


class Bot():
	def __init__(self, x=0,y=0):
		# coords
		self.xy = np.array([x,y])
		self.th = 0.
		self.v = 0.

		# ultra sonic sensors
		self.sonic_sensors = [(0.25,-np.pi/12), (0.25,0.), (0.25,np.pi/12)]


	def sense_distance(self, env):
		measurements = [ sonic_sense(self.xy+r*np.array([np.cos(self.th+a),
														 np.sin(self.th+a)]),
									 self.th+a, env) 
			for (r,a) in self.sonic_sensors]

		return measurements


	def set_path(self, path, w):
		self.path_w = w
		self.path = path
		



def sonic_sense(xy, a, env):
	"""Measures and returns the distance to the closest object within range of 
	ultrasonic sensor. Returns None if no object detected. 
	"""
	return None


