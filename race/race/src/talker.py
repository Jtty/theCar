#!/usr/bin/env python

import rospy
from race.msg import drive_values
from race.msg import drive_param
from std_msgs.msg import Bool

pub = rospy.Publisher('drive_pwm', drive_values, queue_size=10)
em_pub = rospy.Publisher('eStop', Bool, queue_size=10)

# function to map from one range to another, similar to arduino
def arduino_map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# callback function on occurance of drive parameters(angle & velocity)
def callback(data):
	velocity = data.velocity
	angle = data.angle
	print("Velocity: ",velocity,"Angle: ",angle)
	# Do the computation
	pwm1 = arduino_map(velocity,-100,100,6554,13108);
	pwm2 = arduino_map(angle,-100,100,6554,13108);
	msg = drive_values()
	msg.pwm_drive = pwm1
	msg.pwm_angle = pwm2
	pub.publish(msg)

def talker():
	rospy.init_node('serial_talker', anonymous=True)
	em_pub.publish(False)
	rospy.Subscriber("drive_parameters", drive_param, callback)
	
	rospy.spin()

if __name__ == '__main__':
	print("Serial talker initialized")
	talker()


# our version of talker 

# 	#!/usr/bin/env python

# import rospy
# from race.msg import drive_values
# from race.msg import drive_param
# from std_msgs.msg import Bool, String
# """
# What you should do:
#  1. Subscribe to the keyboard messages (If you use the default keyboard.py, you must subcribe to "drive_paramters" which is publishing messages of "drive_param")
#  2. Map the incoming values to the needed PWM values 
#  3. Publish the calculated PWM values on topic "drive_pwm" using custom message drive_values
# drive_values {
#     int16 pwm_drive: [-100, 100]
#     int16 pwm_angle; [6554, 13108]
# }
# """
# pwm_ready = drive_values()
# pub = rospy.Publisher('drive_pwm', drive_values, queue_size=10)
# rospy.init_node('Key_pwm_converter', anonymous=True)

# def convert_and_send(msg):
#     rospy.loginfo(rospy.get_caller_id() + "Value Recvd from keyboard\t Velocity: {0}\tAngle: {1}".format(msg.velocity, msg.angle))
#     pwm_ready.pwm_drive = (msg.velocity+100) * 33 + 6554;
#     pwm_ready.pwm_angle = (msg.angle+100) * 33 + 6554;
#     rospy.loginfo("convert_and_send() is publishing pwm_ready->pwm_drive: {0}\t pwm_angle: {1}".format(pwm_ready.pwm_drive, pwm_ready.pwm_angle))
#     pub.publish(pwm_ready)

# def listener():
#     rospy.Subscriber("drive_parameters", drive_param, convert_and_send)
#     rospy.spin()

# if __name__ == '__main__':
#     try:
#         listener() # Subscribe to keyboard input
        
#     except rospy.ROSInterruptException:
#         pass

