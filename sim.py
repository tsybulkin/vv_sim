from bot import Bot
from obstacles import Person
import numpy as np

SIM_TIME = 10.

def run(dt=0.1, obstacles_nbr=3):
	# init environment and path
	path = [np.array([0.,0]), np.array([0.,10.]),
			np.array([8.,10.]), np.array([8.,14.])]
	path_width = 4.

	# init robot, obstacles, environment
	obstacles = [  Person(path, path_width) for _ in range(obstacles_nbr) ]
	x,y = path[0]
	bot = Bot(x,y)
	bot.set_path(path,path_width)
	env = (bot, obstacles)

	# run simulation
	t = 0.
	sim_log = ([],[ [] for _ in range(obstacles_nbr) ]

	while t < SIM_TIME:
		t += dt
		for pers in obstacles:
			pers.move(env,dt)

		bot.move(env,dt)
		log(sim_log, env)

	damp_as_svg(sim_log)



def log(sim_log, env):
	bot,obstacles = env
	(bot_log, obstacles_logs) = sim_log

	bot_log.append(bot.xy)

	for i in range(len(obstacles)):
		obstacles_logs[i].append(obstacles[i].xy)


def damp_as_svg(sim_log):
	





if __name__ == '__main__':
	run()