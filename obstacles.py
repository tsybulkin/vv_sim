import numpy as np
import random

PAUSE = 1.
RIGHT_90 = np.array([[0., 1.],
					 [-1.,0.]])
LEFT_90 = np.array([[0.,-1.],
					[1., 0.]])

OBJ_MIN_DIST = 0.7


class Person():
	def __init__(self, path, path_w):
		w2 = path_w / 2
		n = np.random.choice(range(len(path)-1))
		x_min = min(path[n][0],path[n+1][0])
		y_min = min(path[n][1],path[n+1][1])
		x_max = max(path[n][0],path[n+1][0])
		y_max = max(path[n][1],path[n+1][1])

		self.path = path[:]
		self.w2 = w2
		self.pause = 0.
		self.log = []

		self.xy = np.array([np.random.uniform(x_min-w2+0.5, x_max+w2-0.5),
							np.random.uniform(y_min-w2+0.5, y_max+w2-0.5)])

		self.v = random.choice([np.array([0.,1.]), np.array([0.,-1.]),
									np.array([1.,0.]), np.array([-1.,0.])])

	def move(self,env,dt):
		xy = self.xy + self.v * dt

		if self.collide(xy, env): self.wait(dt)
		elif self.inside(xy): self.xy = xy
		elif flip_coin(): self.turn_right()
		elif flip_coin(): self.turn_left()
		else: self.turn_back()
		self.log.append(self.xy.copy())

	
	def collide(self, xy, env):
		(bot, people) = env
		for pers in people:
			if pers != self:
				if np.linalg.norm(xy-pers.xy) < OBJ_MIN_DIST:
					return True
		if np.linalg.norm(xy-bot.xy) < OBJ_MIN_DIST: return True
		return False


	def inside(self,xy):
		path = self.path
		return any( self.inside_segment(xy,path[i],path[i+1]) for i in range(len(self.path)-1))

	
	def inside_segment(self,(x,y),xy1,xy2):
		x_min = min(xy1[0],xy2[0])
		y_min = min(xy1[1],xy2[1])
		x_max = max(xy1[0],xy2[0])
		y_max = max(xy1[1],xy2[1])
		w2 = self.w2
		return x >= x_min-w2+0.5 and x <= x_max+w2-0.5 and \
				y >= y_min-w2+0.5 and y <= y_max+w2-0.5

	
	def turn_right(self):
		self.v = RIGHT_90.dot(self.v)


	def turn_left(self):
		self.v = LEFT_90.dot(self.v)


	def turn_back(self):
		self.turn_left()
		self.turn_left()


	def wait(self, dt):
		self.pause += dt
		if self.pause > PAUSE:
			self.pause = np.random.uniform(0.,0.3)
			self.v = random.choice([np.array([0.,1.]), np.array([0.,-1.]),
									np.array([1.,0.]), np.array([-1.,0.])])



def flip_coin(p=0.5): return np.random.uniform() < p


