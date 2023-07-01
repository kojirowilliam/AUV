#!/usr/bin/env python  
import roslib
roslib.load_manifest('mantaray_description')

import rospy
import tf

if __name__ == '__main__':
    rospy.init_node('world_to_base')
    br = tf.TransformBroadcaster()
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        br.sendTransform((0.0, 0.0, 0.0),
                         (0.0, 0.0, 0.0, 1.0),
                         rospy.Time.now(),
                         "mantaray/base_link",
                         "world")
        rate.sleep()