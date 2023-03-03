import rospy
import threading
import time
import numpy as np
import matplotlib.pyplot as plt

from std_msgs.msg import Header
from nav_msgs.msg import Odometry
from uuv_control_msgs.srv import GoTo # , StartWaypointList
from uuv_control_msgs.msg import Waypoint, WaypointSet
	

pos = Odometry()

done = False

def callback_log(data):
	global done
	position = data.pose.pose.position
	rospy.loginfo(position)
	pos = data
	
	#start_set = rospy.ServiceProxy('rexrov2/start_waypoint_list', StartWaypointList)
	
	if not done: 
		wp1 = Waypoint()
		move_point = rospy.ServiceProxy('rexrov2/go_to', GoTo)
		wp1.point.x = -50 + position.x
		wp1.point.y = 0 + position.y
		wp1.point.z = 0 + position.z
		wp1.max_forward_speed = 10.0
		done = True
		move_point(wp1, 1.0, 'cubic')
	

def callback_recieve(msg):
	#rospy.wait_for_service('rexrov2/start_waypoint_set')
	rospy.wait_for_service('rexrov2/go_to')

def listener():
	rospy.init_node('listener', anonymous=True)

	rospy.Subscriber('rexrov2/pose_gt', Odometry, callback_log);
	rospy.spin()


if __name__ == '__main__':
	listener()

	
