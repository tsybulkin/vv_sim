import numpy as np
from sonic import sonic_sense


SONIC_MAX_DISTANCE = 5.0


class Bot():
	def __init__(self, x=0.,y=0.):
		# coords
		self.xy = np.array([x,y])
		self.th = 0.
		self.v = 0.
		self.dv = 0.5  # 1/20 of G
		self.dw = 1.
		self.log = []
		self.sonic_measurements = (None,None,None)

		# ultra sonic sensors
		self.sonic_sensors = [(0.25,np.pi/12), (0.25,0.), (0.25,-np.pi/12)]


	def sense_distance(self, env):
		(_,obstacles) = env

		measurements = [ sonic_sense(self.xy+r*np.array([np.cos(self.th+a),
														 np.sin(self.th+a)]),
									 self.th+a, [ ob.xy for ob in obstacles]) 
			for (r,a) in self.sonic_sensors]

		self.sonic_measurements = tuple(measurements)


	def set_path(self, path, w):
		self.path_w = w
		self.path = path

		
	def move(self, env, dt):
		print "\n",self.xy

		self.sense_distance(env)
		self.control()

		(_,obstacles) = env
		for ob in obstacles:
			if np.linalg.norm(self.xy-ob.xy)<2.:print ob.xy,
		print " "

		self.xy += self.v * np.array([np.cos(self.th),
									np.sin(self.th)]) * dt
		self.log.append((self.xy.copy(), self.sonic_measurements))

	def inside(self):
		path = self.path
		return any( self.inside_segment(path[i],path[i+1]) for i in range(len(self.path)-1))

	
	def inside_segment(self,xy1,xy2):
		x_min = min(xy1[0],xy2[0])
		y_min = min(xy1[1],xy2[1])
		x_max = max(xy1[0],xy2[0])
		y_max = max(xy1[1],xy2[1])
		w2 = self.w2
		x,y = self.xy
		return x >= x_min-w2+0.5 and x <= x_max+w2-0.5 and \
				y >= y_min-w2+0.5 and y <= y_max+w2-0.5

	
	def control(self):
		self.th = np.pi/2
		print self.sonic_measurements

		
		if self.sonic_measurements[1] != None and self.sonic_measurements[1] < 1.5: self.v = 0.
		elif self.sonic_measurements[0] != None and self.sonic_measurements[0] < 1.: self.v = 0.
		elif self.sonic_measurements[2] != None and self.sonic_measurements[2] < 1.: self.v = 0.
		
		elif self.sonic_measurements[1] != None and self.sonic_measurements[1] < 2.5:
			self.v = 0.5
		
		else: 
			self.v = 1.
			
		


