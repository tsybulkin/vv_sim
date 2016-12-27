import numpy as np

## sensor visibility piarameters
ANGLE = np.pi / 3
LENGTH = 5.0
WIDTH = 0.6


def sonic_sense(xy, th, obstacles_xy):
	"""Measures and returns the distance to the closest object within range of 
	ultrasonic sensor. Returns None if no object detected. 
	"""
	## find all normal vectors defining constraints
	n1 = rotate( np.array([np.cos(th+ANGLE/2), np.sin(th+ANGLE/2)]), -np.pi/2 )
	n2 = rotate( np.array([np.cos(th-ANGLE/2), np.sin(th-ANGLE/2)]),  np.pi/2 )
	n3 = rotate( np.array([np.cos(th), np.sin(th)]),  np.pi/2 )

	detected = []
	for ob_xy in obstacles_xy:
		if np.dot(ob_xy-xy, n1) < -0.2: continue
		if np.dot(ob_xy-xy, n2) < -0.2: continue
		if np.dot(ob_xy-xy, n3) < -WIDTH/2: continue
		if np.dot(ob_xy-xy, n3) > WIDTH/2: continue
		if np.linalg.norm(ob_xy-xy) > LENGTH: continue
		detected.append(np.linalg.norm(xy-ob_xy))
	
	if len(detected) == 0: return None
	else:
		detected.sort()
		return detected[0]



def rotate(vect, a):
	return np.array([[np.cos(a), -np.sin(a)],
					 [np.sin(a), np.cos(a)]]).dot(vect)


def test():
	obstacles = [ np.array([0.9, 1.5]), np.array([2.,2.5]), np.array([1.5,4]), 
				np.array([1.5,1.2]) ]
	xy = np.array([1.,1.])
	assert sonic_sense(xy,np.pi/3,obstacles) == np.linalg.norm(np.array([2.,2.5])-xy) 


