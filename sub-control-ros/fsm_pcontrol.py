import rospy
from sensor_msgs.msg import Imu
import custom_util

from fsm_state import fsm_state
from pid_control import pid

class fsm_pcontrol(fsm_state):
    def __init__(self):
        self.name = 'pcontrol'
        # 0 is x, 1 is y, 2 is z
        self.rot_pid = [None]*3
        self.rot_pid[0] = pid(1,0,0)
        self.rot_pid[1] = pid(1,0,0)
        self.rot_pid[2] = pid(1,0,0)

        self.rot_target = [0,0,0]

        self.pos_pid = pid(0,0,0)
        self.thrust_list = [0,0,0,0,0,0,0,0]
        self.rot_euler = [0,0,0]

        self.imu_listener = rospy.Subscriber("mantaray/imu", Imu, self.imu_callback)

    def imu_callback(self, data):
        self.rot_euler = custom_util.euler_from_quaternion(data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w)
        rospy.loginfo(self.rot_euler)

    def set_rot_target(self, r, p, y):
        self.rot_target[0] = r
        self.rot_target[1] = p
        self.rot_target[2] = y

    def run(self, dt):
        for i in range(3):
            self.rot_pid[i].set_state(self.rot_euler[i])
            self.rot_pid[i].update(dt, self.rot_target[i])
        
        self.thrust_list[0] = 0

    def enter(self):
        pass

    def exit(self):
        pass

    def get_thrust_list(self):
        return self.thrust_list

