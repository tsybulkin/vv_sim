from bot import Bot
from obstacles import Person
import numpy as np

WIDTH,HEIGHT = 1100,650
LEFT_MARGIN = 100
TOP_MARGIN = 100

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
	sim_log = ([],[ [] for _ in range(obstacles_nbr) ])

	while t < SIM_TIME:
		t += dt
		for pers in obstacles:
			pers.move(env,dt)

		bot.move(env,dt)
		log(sim_log, env)

	damp_as_svg(sim_log, path, path_width)



def log(sim_log, env):
	bot,obstacles = env
	(bot_log, obstacles_logs) = sim_log

	bot_log.append(bot.xy)

	for i in range(len(obstacles)):
		obstacles_logs[i].append(obstacles[i].xy)


def damp_as_svg(sim_log, path, path_w):

	X_MIN,Y_MIN,X_MAX,Y_MAX = get_mbr(sim_log)
	x_scale = (WIDTH - LEFT_MARGIN) / (X_MAX - X_MIN)
	y_scale = (HEIGHT - TOP_MARGIN) / (Y_MAX - Y_MIN)
	
	f = open("simulation.html",'w')
	f.write("<html>\n<body>\n<svg width='%i' height='%i'>\n" % (WIDTH,HEIGHT))
	
	# draw path
	for n in range(len(path)-1):
		w2 = path_w / 2
		x_min = min(path[n][0],path[n+1][0])
		y_min = min(path[n][1],path[n+1][1])
		x_max = max(path[n][0],path[n+1][0])
		y_max = max(path[n][1],path[n+1][1])

		f.write(svg_rect((0, y_max+w2), (x_max-x_min+2*w2, y_max-y_min+2*w2), 'rgb(200,200,200)', x_scale,y_scale))

	# draw bot

	# draw obstacles

	f.write("</svg>\n</body>\n</html>")
	f.close()


def svg_rect((x1,y1), (x2,y2), color, x_scale, y_scale):
	X,Y = px((x1,y1),x_scale,y_scale)
	W,H = px((x2-x1,y2-y1),x_scale,y_scale)
	return "<rect x='%i' y='%i' width='%i' height='%i' \
			style='fill:%s' />\n" % (X,Y,W,H,color)


def px(xy,x_scale,y_scale):
	x = int(round(xy[0]*x_scale))
	y = HEIGHT - int(round(xy[1]*y_scale))
	return LEFT_MARGIN+x, TOP_MARGIN+y


def get_mbr((bot_log, obstacles_logs)):
	x_min = min( xy[0] for xy in bot_log)
	y_min = min( xy[1] for xy in bot_log)
	x_max = max( xy[0] for xy in bot_log)
	y_max = max( xy[1] for xy in bot_log)
	for log in obstacles_logs:
		x_min = min(x_min, min(xy[0] for xy in log))
		y_min = min(y_min, min(xy[1] for xy in log))
		x_max = max(x_max, max(xy[0] for xy in log))
		y_max = max(y_max, max(xy[1] for xy in log))
	return (x_min,y_min,x_max,y_max)


if __name__ == '__main__':
	run()