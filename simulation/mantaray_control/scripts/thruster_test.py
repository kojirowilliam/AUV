#!/usr/bin/env python

import rospy

import rospy
import math

import time

from uuv_gazebo_ros_plugins_msgs.msg import FloatStamped

def test(num, thruster):
    rospy.init_node('thruster_test_pub', anonymous = True)
    
    if num == 0:
        pub = rospy.Publisher('/mantaray/thrusters/0/input', FloatStamped, queue_size=10)
    elif num == 1:
        pub = rospy.Publisher('/mantaray/thrusters/1/input', FloatStamped, queue_size=10)
    elif num == 2:
        pub = rospy.Publisher('/mantaray/thrusters/2/input', FloatStamped, queue_size=10)
    elif num == 3:
        pub = rospy.Publisher('/mantaray/thrusters/3/input', FloatStamped, queue_size=10)
    elif num == 4:
        pub = rospy.Publisher('/mantaray/thrusters/4/input', FloatStamped, queue_size=10)
    elif num == 5:
        pub = rospy.Publisher('/mantaray/thrusters/5/input', FloatStamped, queue_size=10)
    elif num == 6:
        pub = rospy.Publisher('/mantaray/thrusters/6/input', FloatStamped, queue_size=10)
    elif num == 7:
        pub = rospy.Publisher('/mantaray/thrusters/7/input', FloatStamped, queue_size=10)
   
    while not rospy.is_shutdown():
        time.sleep(3) # has to wait before running 
        t = FloatStamped()
        t.header.stamp = rospy.Time.now()
        t.data = thruster
        pub.publish(t)

        rate = rospy.Rate(10) # 10hz
        rate.sleep()



def config1():
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
        
        time.sleep(3) # has to wait before running 
        t0 = FloatStamped()
        t0.header.stamp = rospy.Time.now()
        t0.data = 100 # This is what controls how much thrust is exerted
        pub0.publish(t0)
        time.sleep(3)        
        t1 = FloatStamped()
        t1.header.stamp = rospy.Time.now()
        t1.data = 100
        pub1.publish(t1)
        time.sleep(3)
        t2 = FloatStamped()
        t2.header.stamp = rospy.Time.now()
        t2.data = 100
        pub2.publish(t2)
        time.sleep(3)
        t3 = FloatStamped()
        t3.header.stamp = rospy.Time.now()
        t3.data = 100
        pub3.publish(t3)
        time.sleep(3)
        t4 = FloatStamped()
        t4.header.stamp = rospy.Time.now()
        t4.data = 100
        pub4.publish(t4)
        time.sleep(3)
        t5 = FloatStamped()
        t5.header.stamp = rospy.Time.now()
        t5.data = 100
        pub5.publish(t5)
        time.sleep(3)
        t6 = FloatStamped()
        t6.header.stamp = rospy.Time.now()
        t6.data = 100
        pub6.publish(t6)
        time.sleep(3)
        t7 = FloatStamped()
        t7.header.stamp = rospy.Time.now()
        t7.data = 100
        pub7.publish(t7)
        

        rate = rospy.Rate(10) # 10hz
        rate.sleep()
    
    

if __name__ == '__main__':
    try:
        config1()
    except rospy.ROSInterruptException:
        print("ERROR")
        pass