#!/usr/bin/env python

import numpy as np
import rospy
import math
import pyzed.sl as sl
from std_msgs.msg import String

def img_data_publisher():
    pub = rospy.Publisher('img_data', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    
    # Create a ZED camera
    zed = sl.Camera()

    # Create configuration parameters
    init_params = sl.InitParameters()
    init_params.sdk_verbose = True # Enable the verbose mode
    init_params.depth_mode = sl.DEPTH_MODE.PERFORMANCE # Set the depth mode to performance (fastest)

    # Open the camera
    err = zed.open(init_params)
    if (err!=sl.ERROR_CODE.SUCCESS):
        exit(-1)
        
        
    # Create and set RuntimeParameters after opening the camera
    runtime_parameters = sl.RuntimeParameters()
    runtime_parameters.sensing_mode = sl.SENSING_MODE.STANDARD  # Use STANDARD sensing mode
    
    # Setting the depth confidence parameters
    runtime_parameters.confidence_threshold = 100
    runtime_parameters.textureness_confidence_threshold = 100
    
    while not rospy.is_shutdown():
        image = sl.Mat()
        depth = sl.Mat()
        point_cloud = sl.Mat()
        
        if(zed.grab() == sl.ERROR_CODE.SUCCESS) :
            zed.retrieve_measure(depth, sl.MEASURE.DEPTH)
            zed.retrieve_image(image, sl.VIEW.LEFT)
            zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA)
            
        
        x = round(image.get_width() / 2)
        y = round(image.get_height() / 2)
        
        err, point_cloud_value = point_cloud.get_value(x, y)
        
        distance = math.sqrt(point_cloud_value[0] * point_cloud_value[0] + point_cloud_value[1] * point_cloud_value[1] + point_cloud_value[2] * point_cloud_value[2])
        
        message = "distance to point at {},{}: {}".format(x,y,distance)
        
        if np.isnan(distance) or np.isinf(distance):
            rospy.loginfo("failed")
            pub.publish("failed")
        else:
            rospy.loginfo(message)
            pub.publish(message)

        rate.sleep()

if __name__ == '__main__':
    try:
        img_data_publisher()
    except rospy.ROSInterruptException:
        pass
