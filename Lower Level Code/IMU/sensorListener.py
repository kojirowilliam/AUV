import rospy
from beginner_tutorials.msg import Sensor

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.baro)

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('sensorListener', anonymous=True)

    rospy.Subscriber('sensorChatter', Sensor, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
