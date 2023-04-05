import rospy

#!/usr/bin/env python

import numpy as np
import rospy

from uuv_gazebo_ros_plugins_msgs.msg import FloatStamped

from std_msgs.msg import String, Header

def thruster_publisher():
    rospy.init_node('lit', anonymous=True)
    pub0 = rospy.Publisher('/rexrov2/thrusters/0/input', FloatStamped, queue_size=10)
    pub1 = rospy.Publisher('/rexrov2/thrusters/1/input', FloatStamped, queue_size=10)
    pub2 = rospy.Publisher('/rexrov2/thrusters/2/input', FloatStamped, queue_size=10)
    pub3 = rospy.Publisher('/rexrov2/thrusters/3/input', FloatStamped, queue_size=10)
    pub4 = rospy.Publisher('/rexrov2/thrusters/4/input', FloatStamped, queue_size=10)
    pub5 = rospy.Publisher('/rexrov2/thrusters/5/input', FloatStamped, queue_size=10)
    pub6 = rospy.Publisher('/rexrov2/thrusters/6/input', FloatStamped, queue_size=10)
    pub7 = rospy.Publisher('/rexrov2/thrusters/7/input', FloatStamped, queue_size=10)

    while not rospy.is_shutdown():
        t0 = FloatStamped()
        t0.header.stamp = rospy.Time.now()
        t0.data = 0
        pub0.publish(t0)
        t1 = FloatStamped()
        t1.header.stamp = rospy.Time.now()
        t1.data = 0
        pub1.publish(t1)
        t2 = FloatStamped()
        t2.header.stamp = rospy.Time.now()
        t2.data = 0
        pub2.publish(t2)
        



        rate = rospy.Rate(10) # 10hz
        rate.sleep()
    
    

if __name__ == '__main__':
    try:
        thruster_publisher()
    except rospy.ROSInterruptException:
        print("ERROR")
        pass