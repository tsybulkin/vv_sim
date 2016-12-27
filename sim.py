from bot import Bot
from obstacles import Person
import numpy as np

WIDTH,HEIGHT = 1100, 650
LEFT_MARGIN = 100
TOP_MARGIN = 100
PERSON_RADIUS = 0.3
BOT_RADIUS = 0.25

SIM_TIME = 15.


def run(dt=0.1, obstacles_nbr=10):
	# init environment and path
	path = [np.array([0.,0.]), np.array([0.,10.]),
			np.array([8.,10.]), np.array([8.,14.])]
	path_width = 4.

	# init robot, obstacles, environment
	obstacles = []
	x,y = path[0]
	bot = Bot(x,y)

	bot.set_path(path,path_width)
	env = (bot, obstacles)

	while len(obstacles) < obstacles_nbr:
		pers = Person(path, path_width)
		if pers.collide(pers.xy, env): continue
		obstacles.append(pers)


	# run simulation
	t = 0.
	sim_log = ([],[ [] for _ in range(obstacles_nbr) ])

	while t < SIM_TIME:
		t += dt
		for pers in obstacles:
			pers.move(env,dt)

		bot.move(env,dt)
		log(sim_log, env)

	damp_as_svg(sim_log, path, path_width, dt)


def log(sim_log, env):
	bot,obstacles = env
	(bot_log, obstacles_logs) = sim_log

	bot_log.append(bot.xy.copy())

	for i in range(len(obstacles)):
		obstacles_logs[i].append(obstacles[i].xy.copy())


def damp_as_svg((bot_log, obstacles_logs), path, path_w, dt):
	X_MIN,Y_MIN,X_MAX,Y_MAX = get_mbr((bot_log, obstacles_logs))
	x_scale = (WIDTH - LEFT_MARGIN) / (X_MAX - X_MIN)
	y_scale = (HEIGHT - 2*TOP_MARGIN) / (Y_MAX - Y_MIN)
	scale = min(x_scale,y_scale)

	b_log, ob_logs = (map(lambda xy:(LEFT_MARGIN+int((xy[0]-X_MIN)*scale), HEIGHT-int((xy[1]-Y_MIN)*scale)),bot_log), \
					[ map(lambda xy:(LEFT_MARGIN+int((xy[0]-X_MIN)*scale), HEIGHT-int((xy[1]-Y_MIN)*scale)), log)
						for log in obstacles_logs] )
	
	f = open("simulation.html",'w')
	f.write("<html>\n<body>\n<svg width='%i' height='%i'>\n" % (WIDTH,HEIGHT))
	
	# draw path
	for n in range(len(path)-1):
		w2 = path_w / 2
		x1 = min(path[n][0],path[n+1][0])-w2
		y1 = min(path[n][1],path[n+1][1])-w2
		x2 = max(path[n][0],path[n+1][0])+w2
		y2 = max(path[n][1],path[n+1][1])+w2

		f.write(svg_rect(LEFT_MARGIN+int((x1-X_MIN)*scale), HEIGHT-int((y2-Y_MIN)*scale), int((x2-x1)*scale), int((y2-y1)*scale), 'rgb(200,200,200)'))

	# draw bot
	cx,cy = b_log[0]
	bw = int(BOT_RADIUS*scale)
	f.write("<circle cx='%i' cy='%i' r='%i' fill='green'>\n" %(cx,cy,bw))
	T = 0.
	for x,y in b_log:
		f.write("\t<set attributeName='cx' attributeType='XML'\n \
     		to='%i' begin='%.2fs' dur='%.2fs' />\n" %(x,T,dt) )
		f.write("\t<set attributeName='cy' attributeType='XML'\n \
     		to='%i' begin='%.2fs' dur='%.2fs' />\n" %(y,T,dt) )
		T += dt
	f.write("</circle>\n")

	# draw obstacles
	pw = int(PERSON_RADIUS*scale)
	for ob in ob_logs:
		cx,cy = ob[0]
		f.write("<circle cx='%i' cy='%i' r='%i' fill='red'>\n" %(cx,cy,pw))
		T = 0.
		for x,y in ob:
			f.write("\t<set attributeName='cx' attributeType='XML'\n \
         		to='%i' begin='%.2fs' dur='%.2fs' />\n" %(x,T,dt) )
			f.write("\t<set attributeName='cy' attributeType='XML'\n \
         		to='%i' begin='%.2fs' dur='%.2fs' />\n" %(y,T,dt) )
			T += dt
		f.write("</circle>\n")


	f.write("</svg>\n</body>\n</html>")
	f.close()


def svg_rect(x,y, w,h, color):
	return "<rect x='%i' y='%i' width='%i' height='%i' \
			style='fill:%s' />\n" % (x,y,w,h,color)



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