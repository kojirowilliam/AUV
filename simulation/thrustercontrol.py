import rospy
from pid_control import pid

#!/usr/bin/env python

import numpy as np
import rospy
import math

import time

from uuv_gazebo_ros_plugins_msgs.msg import FloatStamped
from nav_msgs.msg import Odometry
from std_msgs.msg import String, Header

#t0 - center front left/right strafe
#t1 - top center back up/down
#t2 - top right front up/down
#t3 - top left front down/up
#t4 - back left forward/back
#t5 - back right forward/back

# altitude control: up - t1+, t2+, t3-
# forward/backward: forward - t4+, t5+
# pitch: up - t1+, t2+, t3-
# yaw: left - t0+, t4+, t5-
# strafe: left - t0+, t4+, t5- 
# roll: clockwise - t2+, t3+

pid_forward = pid(10, 0, 0)
pid_alt = pid(0,0,0)
pid_pitch = pid(0,0,0)
pid_yaw = pid(50,0.01,200)
pid_roll = pid(0,0,0)
pid_strafe = pid(0,0,0)

position = [0,0,0]
orientation = [0,0,0,0]
def pose_listener(data):
    pose = data.pose.pose.position
    global position
    position[0] = pose.x
    position[1] = pose.y
    position[2] = pose.z

    orien = data.pose.pose.orientation
    global orientation
    orientation[0] = orien.x
    orientation[1] = orien.y
    orientation[2] = orien.z
    orientation[3] = orien.w
    
def to_euler_angles (orientation):
    euler = [0,0,0]

    x = orientation[0]
    y = orientation[1]
    z = orientation[2]
    w = orientation[3]

    # setting roll
    sinr_cosp = 2*(w*x + y*z)
    cosr_cosp = 1 - 2*(x*x + y*y)
    euler[0] = math.atan2(sinr_cosp, cosr_cosp)

    # setting pitch
    sinp = math.sqrt(1 + 2*(w*y - x*z))
    cosp = math.sqrt(1 - 2*(w*y + x*z))
    euler[1] = math.atan2(sinp, cosp) - math.pi / 2

    # setting yaw
    siny_cosp = 2*(w*z + x*y)
    cosy_cosp = 1 - 2*(y*y + z*z)
    euler[2] = math.atan2(siny_cosp, cosy_cosp)

    return euler

def thruster_publisher(name):
    global position
    global orientation
    rospy.init_node('lit', anonymous=True)

    rospy.Subscriber('/' + name + '/pose_gt', Odometry, pose_listener)    
    pub0 = rospy.Publisher('/' + name + '/thrusters/0/input', FloatStamped, queue_size=10)
    pub1 = rospy.Publisher('/' + name + '/thrusters/1/input', FloatStamped, queue_size=10)
    pub2 = rospy.Publisher('/' + name + '/thrusters/2/input', FloatStamped, queue_size=10)
    pub3 = rospy.Publisher('/' + name + '/thrusters/3/input', FloatStamped, queue_size=10)
    pub4 = rospy.Publisher('/' + name + '/thrusters/4/input', FloatStamped, queue_size=10)
    pub5 = rospy.Publisher('/' + name + '/thrusters/5/input', FloatStamped, queue_size=10)
    pub6 = rospy.Publisher('/' + name + '/thrusters/6/input', FloatStamped, queue_size=10)
    pub7 = rospy.Publisher('/' + name + '/thrusters/5/input', FloatStamped, queue_size=10)
    
    

    time_last = time.time()

    while not rospy.is_shutdown():
        
        t = time.time()
        dt = t - time_last

        t0 = FloatStamped()
        t0.header.stamp = rospy.Time.now()
        t0.data = pid_yaw.get_output() + pid_strafe.get_output()
        pub0.publish(t0)
        t1 = FloatStamped()
        t1.header.stamp = rospy.Time.now()
        t1.data = pid_pitch.get_output() + pid_alt.get_output()
        pub1.publish(t1)
        t2 = FloatStamped()
        t2.header.stamp = rospy.Time.now()
        t2.data = pid_pitch.get_output() + pid_roll.get_output() + pid_alt.get_output()
        pub2.publish(t2)
        t3 = FloatStamped()
        t3.header.stamp = rospy.Time.now()
        t3.data = -pid_pitch.get_output() + pid_roll.get_output() - pid_alt.get_output()
        pub3.publish(t3)
        t4 = FloatStamped()
        t4.header.stamp = rospy.Time.now()
        t4.data = pid_forward.get_output() + pid_yaw.get_output()
        pub4.publish(t4)
        t5 = FloatStamped()
        t5.header.stamp = rospy.Time.now()
        t5.data = -pid_forward.get_output() - pid_yaw.get_output()
        pub5.publish(t5)
        
        

        target = [100,0]

        distance = math.sqrt((target[0] - position[0])**2 + (target[1] - position[1])**2)
        angle_to_target  = math.atan2(target[1] - position[1], target[0] - position[0])
        euler_angles = to_euler_angles(orientation)

        pid_forward.set_value(distance)
        pid_alt.set_value(0)
        pid_strafe.set_value(0)
        pid_roll.set_value(euler_angles[0])
        pid_pitch.set_value(euler_angles[1])
        pid_yaw.set_value(angle_to_target - euler_angles[2])

        print(angle_to_target - euler_angles[2])

        pid_forward.update(0, dt)
        pid_alt.update(0, dt)
        pid_strafe.update(0, dt)
        pid_pitch.update(0, dt)
        pid_yaw.update(0,dt)
        pid_roll.update(0,dt)

        time_last = t

        rate = rospy.Rate(10) # 10hz
        rate.sleep()
    
    

if __name__ == '__main__':
    try:
        thruster_publisher()
    except rospy.ROSInterruptException:
        print("ERROR")
        pass