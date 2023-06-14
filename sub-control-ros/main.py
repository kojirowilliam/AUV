import rospy
import time
from fsm import fsm
from fsm_basic import fsm_basic
from fsm_pcontrol import fsm_pcontrol
from uuv_gazebo_ros_plugins_msgs.msg import FloatStamped
from nav_msgs.msg import Odometry
from std_msgs.msg import String, Header

running = True

SUB_NAME = "mantaray"
THRUSTER_COUNT = 8

fsm = fsm()

def thruster_publisher(name, fsm):
    
    rospy.init_node('lit', anonymous=True) 

    pub = []

    for i in range(THRUSTER_COUNT):
        pub.append(rospy.Publisher('/' + name + '/thrusters/'+str(i)+'/input', FloatStamped, queue_size=10))
    

    time_last = time.time()
    while not rospy.is_shutdown():
        for i in range(THRUSTER_COUNT):
            fs = FloatStamped()
            fs.header.stamp = rospy.Time.now()
            fs.data = fsm.get_state().get_thrust_list()[i]
            pub[i].publish(fs)

        rate = rospy.Rate(10) # 10hz
        rate.sleep()


def stop():
    print("stop")
    running = False



if __name__ == "__main__":
    thruster_publisher(SUB_NAME, fsm)
