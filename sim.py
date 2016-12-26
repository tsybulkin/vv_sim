from bot import Bot
from obstacles import Person
import numpy as np



def run():
	# init environment and path
	path = [np.array([0.,0]), np.array([0.,10.]),
			np.array([8.,10.]), np.array([8.,14.])]
	path_width = 4.

	# init robot, obstacles, environment
	obstacles = [  Person(path, path_width) for _ in range(obstacles_nbr) ]

	# run simulation



if __name__ == '__main__':
	run()