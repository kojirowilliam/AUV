#!/usr/bin/env python


import numpy as np
import rospy
import math
import pyzed.sl as sl
from std_msgs.msg import String

def shutdown_hook():
    zed.disable_positional_tracking("test1.area")
    

def talker():
    pub = rospy.Publisher('pos_data', String, queue_size=10)
    rospy.init_node('talker', anonymous=True, disable_signals=False)
    rospy.on_shutdown(shutdown_hook)
    rate = rospy.Rate(10) # 10hz

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
    
    tracking_parameters = sl.PositionalTrackingParameters()
    err = zed.enable_positional_tracking(tracking_parameters)
    tracking_parameters.area_file_path = "test.area"
    
    if err != sl.ERROR_CODE.SUCCESS:
        exit(1)
    
    mapping_parameters = sl.SpatialMappingParameters()
    err = zed.enable_spatial_mapping(mapping_parameters)
    if err != sl.ERROR_CODE.SUCCESS:
        exit(1)
    
    # Setting the depth confidence parameters
    runtime_parameters.confidence_threshold = 100
    runtime_parameters.textureness_confidence_threshold = 100
    
    
    count = 0
    
    while not rospy.is_shutdown():
        zed_pose = sl.Pose()
        
        #count = count + 1
        if count == 100:
            rospy.signal_shutdown("done")
        
        if(zed.grab() == sl.ERROR_CODE.SUCCESS) :
            # Get the pose of the camera relative to the world frame
            state = zed.get_position(zed_pose, sl.REFERENCE_FRAME.WORLD)
            # Display translation and timestamp
            py_translation = sl.Translation()
            tx = round(zed_pose.get_translation(py_translation).get()[0]*0.001, 3)
            ty = round(zed_pose.get_translation(py_translation).get()[1]*0.001, 3)
            tz = round(zed_pose.get_translation(py_translation).get()[2]*0.001, 3)
            
            #Display orientation quaternion
            py_orientation = sl.Orientation()
            ox = round(zed_pose.get_orientation(py_orientation).get()[0], 3)
            oy = round(zed_pose.get_orientation(py_orientation).get()[1], 3)
            oz = round(zed_pose.get_orientation(py_orientation).get()[2], 3)
            ow = round(zed_pose.get_orientation(py_orientation).get()[3], 3)
        
        position_str = "tran ({},{},{}) ori ({},{},{},{}), tracking_state:".format(tx,ty,tz,ox,oy,oz,ow) + str(state)
        rospy.loginfo(position_str)
        pub.publish(position_str)
        rate.sleep()

if __name__ == '__main__':
    # Create a ZED camera
    zed = sl.Camera()
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
    
