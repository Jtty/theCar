#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import LaserScan
from race.msg import pid_input

desired_trajectory = .7
vel = 18
turning = 0

pub = rospy.Publisher('error', pid_input, queue_size=10)

##	Input: 	data: Lidar scan data
##			theta: The angle at which the distance is requried
##	OUTPUT: distance of scan at angle theta
def getRange(data,theta):
# Find the index of the arary that corresponds to angle theta.
# Return the lidar scan value at that index
# Do some error checking for NaN and ubsurd values
## Your code goes here
	rad = math.radians(theta) - math.pi/2 - data.angle_min
	idx = int(round(rad/data.angle_increment))

	return data.ranges[idx]

def doMath(theta, Q, P, R):
	swing = math.radians(theta)
	littler = 90 + theta
	littlec = math.sqrt(math.pow(P, 2) + math.pow(Q, 2) - 2 * P * Q * math.cos(swing))
	bigx = Q - R
	littlex = math.asin((bigx * math.sin(math.radians(littler)))/littlec)
	littley = 90 - littlex
	return math.sin(math.radians(littley)) * P


def callback(data):
	theta = 50
	a = getRange(data,theta) #our Hypotenuse
	b = getRange(data,0) #our straight to the right
	c = getRange(data,40) #40 degree sample
	swing = math.radians(theta)
	realHypotenuse = b/math.cos(swing) #calculated if we were straight
	#math shit
	#realDistance = doMath(theta, a, b, realHypotenuse)


	#print("realDistance: ", realDistance)
	## Your code goes here
	print("dist[0]", b)
	print("dist[40]",c)
	print("dist[50]", a)


	#error = -217.12 * math.pow(dist, 3) + 455.952 * math.pow(dist, 2) - 406.506 * dist + 135.61
	
	

	alpha = math.atan((a*math.cos(swing)-b)/(a*math.sin(swing)))
	dist = b*math.cos(alpha)
	print("distance", dist)
	function = 482.565 * math.pow(dist,3) - 1013.39 * math.pow(dist,2) + 791.781 * dist - 223.207 
	shouldTurn  = False
		

	if(c > a): #change us to turning state
		shouldTurn = True

	if(shouldTurn):
		error = 90
	elif(a < realHypotenuse):
		#angled towards the wall
		print("Angled Right")
		if(dist < desired_trajectory):
			#too close
			print("Toooo Close")
			#turn away from wall (left)
			error = function
		else:
			#far away
			#go straight
			error = 0
	elif(a >= realHypotenuse):
		#angled away from wall
		print("Angled Left")
		if(dist < desired_trajectory):
			#too close
			#go straight
			error = 0
		else:
			#far away
			print("Far Away")
			#turn toward wall (right)
			error = function
	#error = dist - desired_trajectory
	
	## END

	msg = pid_input()
	msg.pid_error = error
	msg.pid_vel = vel
	pub.publish(msg)
	# original error func -(-217.12 * math.pow(dist, 3) + 455.952 * math.pow(dist, 2) - 406.506 * dist + 135.61)



if __name__ == '__main__':
	print("Laser node started")
	rospy.init_node('dist_finder',anonymous = True)
	rospy.Subscriber("scan",LaserScan,callback)
	rospy.spin()
