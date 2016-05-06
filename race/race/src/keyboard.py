#!/usr/bin/env python

import rospy
from race.msg import drive_param
import curses
#import signal
#TIMEOUT = 0.1 # number of seconds your want for timeout
forward = 0;
left = 0;

# def interrupted(signum, frame):
#     "called when read times out"
#     global forward
#     forward = 0
#     global left
#     left = 0
#     stdscr.addstr(2, 20, "Stop")
#     stdscr.addstr(2, 25, '%.2f' % forward)
#     stdscr.addstr(3, 20, "Stop")
#     stdscr.addstr(3, 25, '%.2f' % left)
# signal.signal(signal.SIGALRM, interrupted)

# def input():
#     try:
#             foo = stdscr.getch()
#             return foo
#     except:
#             # timeout
#             return

stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)
rospy.init_node('keyboard_talker', anonymous=True)
pub = rospy.Publisher('drive_parameters', drive_param, queue_size=10)

# set alarm
#signal.alarm(TIMEOUT)
#s = input()
# disable the alarm after success
#signal.alarm(0)
#print 'You typed', s

stdscr.refresh()

key = ''
while key != ord('q'):
#	signal.setitimer(signal.ITIMER_REAL,0.05)
#	key = input()
	key = stdscr.getch()
	stdscr.refresh()
#	signal.alarm(0)
	if key == curses.KEY_UP: 
		forward = forward + 0.1;
		stdscr.addstr(2, 20, "Up  ")
		stdscr.addstr(2, 25, '%.2f' % forward)
		stdscr.addstr(5, 20, "    ")
	elif key == curses.KEY_DOWN:
		forward = forward - 0.1; 
		stdscr.addstr(2, 20, "Down")
		stdscr.addstr(2, 25, '%.2f' % forward)
		stdscr.addstr(5, 20, "    ")
	if key == curses.KEY_LEFT:
		left = left - 0.1; 
		stdscr.addstr(3, 20, "left")
		stdscr.addstr(3, 25, '%.2f' % left)
		stdscr.addstr(5, 20, "    ")
	elif key == curses.KEY_RIGHT:
		left = left + 0.1; 
		stdscr.addstr(3, 20, "rgt ")
		stdscr.addstr(3, 25, '%.2f' % left)
		stdscr.addstr(5, 20, "    ")
	if key == curses.KEY_DC:
		left = 0
		forward = 0
		stdscr.addstr(5, 20, "Stop")
	msg = drive_param()
	msg.velocity = forward
	msg.angle = left
	pub.publish(msg)
curses.endwin()

# Our version of keyboard -------------
# #!/usr/bin/env python

# import rospy
# from race.msg import drive_param # import the custom message
# import curses
# forward = 0;
# left = 0;

# stdscr = curses.initscr()
# curses.cbreak()
# stdscr.keypad(1)
# rospy.init_node('keyboard', anonymous=True)
# pub = rospy.Publisher('drive_parameters', drive_param, queue_size=10)

# stdscr.refresh()

# key = ''
# while key != ord('q'):
#   key = stdscr.getch()
#   stdscr.refresh()
        
#   # fill in the conditions to increment/decrement throttle/steer

#   if key == curses.KEY_UP:
#     forward += 1
#   elif key == curses.KEY_DOWN:
#     forward -= 1
#   if key == curses.KEY_LEFT:
#     left += 1
#   elif key == curses.KEY_RIGHT:
#     left -= 1
#   elif key == curses.KEY_DC or key == ord(' '):
#   # this key will center the steer and throttle
#     forward -= forward
#     left -= left

#   msg = drive_param()
#   msg.velocity = forward
#   msg.angle = left
#   pub.publish(msg)

# curses.endwin()
