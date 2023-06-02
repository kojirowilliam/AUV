# Useful tutorial: http://wiki.ros.org/cv_bridge/Tutorials/ConvertingBetweenROSImagesAndOpenCVImagesPython


import rospy
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2 as cv


def callback(data):
    try:
      cv_image = bridge.imgmsg_to_cv2(data, "passthrough")
      frame = cv.resize(cv_image, (400,300), interpolation=cv.INTER_AREA)
      img_blur = cv.GaussianBlur(frame, (3,3), 0)
      edges = cv.Canny(image=img_blur, threshold1 = 100, threshold2 = 200)
      cv.imshow('edges', edges)
    except CvBridgeError as e:
      print(e)
    
    (rows,cols,channels) = cv_image.shape
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame

    orb = cv.ORB_create()
    orb.setEdgeThreshold(5)
    kp = orb.detect(gray,None)
    img2 = cv.drawKeypoints(gray, kp, None, color=(0,255,0), flags=0)
    cv.imshow('Input', img2)

    # cv.imshow('frame', gray)
    
    rospy.loginfo("I heard %s", gray)
    cv.waitKey(1)
    
def listener():
    rospy.init_node('image_capture', anonymous=True)

    rospy.Subscriber("/rexrov2/rexrov2/camera/camera_image", Image, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.sleep(0.01)
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