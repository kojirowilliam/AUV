# Useful tutorial: http://wiki.ros.org/cv_bridge/Tutorials/ConvertingBetweenROSImagesAndOpenCVImagesPython


import rospy
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2 as cv


def callback(data):
    try:
      cv_image = bridge.imgmsg_to_cv2(data, "passthrough")
    except CvBridgeError as e:
      print(e)
    
    (rows,cols,channels) = cv_image.shape
    gray = cv.cvtColor(cv_image, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv.imshow('frame', gray)
    
    rospy.loginfo("I heard %s", gray)
    cv.waitKey()
    
def listener():
    rospy.init_node('image_capture', anonymous=True)

    rospy.Subscriber("/rexrov2/rexrov2/camera/camera_image", Image, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    bridge = CvBridge()
    listener()

# Example Publisher Code:

# def talker():
#     pub = rospy.Publisher('chatter', String, queue_size=10)
#     rospy.init_node('talker', anonymous=True)
#     rate = rospy.Rate(10) # 10hz
#     while not rospy.is_shutdown():
#         hello_str = "hello world %s" % rospy.get_time()
#         rospy.loginfo(hello_str)
#         pub.publish(hello_str)
#         rate.sleep()
# if __name__ == '__main__':
#     try:
#         talker()
#     except rospy.ROSInterruptException:
#         pass