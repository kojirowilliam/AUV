#!/usr/bin/env python

import rospy

import rospy
import math

import time

from uuv_gazebo_ros_plugins_msgs.msg import FloatStamped
from nav_msgs.msg import Odometry
from std_msgs.msg import String, Header

def thruster_publisher():
    rospy.init_node('thruster_tester_pub', anonymous=True)

    pub0 = rospy.Publisher('/mantaray/thrusters/0/input', FloatStamped, queue_size=10)
    pub1 = rospy.Publisher('/mantaray/thrusters/1/input', FloatStamped, queue_size=10)
    pub2 = rospy.Publisher('/mantaray/thrusters/2/input', FloatStamped, queue_size=10)
    pub3 = rospy.Publisher('/mantaray/thrusters/3/input', FloatStamped, queue_size=10)
    pub4 = rospy.Publisher('/mantaray/thrusters/4/input', FloatStamped, queue_size=10)
    pub5 = rospy.Publisher('/mantaray/thrusters/5/input', FloatStamped, queue_size=10)
    pub6 = rospy.Publisher('/mantaray/thrusters/6/input', FloatStamped, queue_size=10)
    pub7 = rospy.Publisher('/mantaray/thrusters/7/input', FloatStamped, queue_size=10)

    time_last = time.time()

    while not rospy.is_shutdown():
        
        t = time.time()

        t0 = FloatStamped()
        t0.header.stamp = rospy.Time.now()
        t0.data = 1000
        pub0.publish(t0)
        time.sleep(5)
        t1 = FloatStamped()
        t1.header.stamp = rospy.Time.now()
        t1.data = 1000
        pub1.publish(t1)
        time.sleep(5)
        t2 = FloatStamped()
        t2.header.stamp = rospy.Time.now()
        t2.data = 1000
        pub2.publish(t2)
        time.sleep(5)
        t3 = FloatStamped()
        t3.header.stamp = rospy.Time.now()
        t3.data = 1000
        pub3.publish(t3)
        time.sleep(5)
        t4 = FloatStamped()
        t4.header.stamp = rospy.Time.now()
        t4.data = 1000
        pub4.publish(t4)
        time.sleep(5)
        t5 = FloatStamped()
        t5.header.stamp = rospy.Time.now()
        t5.data = 1000
        pub5.publish(t5)
        time.sleep(5)
        t6 = FloatStamped()
        t6.header.stamp = rospy.Time.now()
        t6.data = 1000
        pub5.publish(t6)
        time.sleep(5)
        t7 = FloatStamped()
        t7.header.stamp = rospy.Time.now()
        t7.data = 1000
        pub5.publish(t7)
        time.sleep(20)

        rate = rospy.Rate(10) # 10hz
        rate.sleep()
    
    

if __name__ == '__main__':
    try:
        thruster_publisher()
    except rospy.ROSInterruptException:
        print("ERROR")
        pass