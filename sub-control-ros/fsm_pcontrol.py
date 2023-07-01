import rospy
from sensor_msgs.msg import Imu
from tf.transformations import quaternion_from_euler
import keyboard
from qp_attitude_controller import QuaternionAttitudeController
from fsm_state import fsm_state
from pid_control import pid

IMU_TOPIC = "mantaray/imu"
KF_ANGULAR = 120

class fsm_pcontrol(fsm_state):
    def __init__(self):
        self.name = 'pcontrol'
        # 0 is x, 1 is y, 2 is z
        self.rot_pid = [None]*3
        self.rot_pid[0] = pid(150,0,0)
        self.rot_pid[1] = pid(0,0,0)
        self.rot_pid[2] = pid(150,0,0) #150, 0 ,0
        
        self.qp_attitude_controller = QuaternionAttitudeController(0.1)

        self.rot_target = [0,0,0,0]

        self.pos_pid = pid(0,0,0)
        self.thrust_list = [0,0,0,0,0,0,0,0]
        self.rot_quat = [0,0,0,0]
        self.rot_vel = [0,0,0]

        self.imu_listener = rospy.Subscriber(IMU_TOPIC, Imu, self.imu_callback)

    def imu_callback(self, data):
        self.rot_quat[0] = data.orientation.x
        self.rot_quat[1] = data.orientation.y
        self.rot_quat[2] = data.orientation.z
        self.rot_quat[3] = data.orientation.w
        
        self.rot_vel[0] = data.angular_velocity.x
        self.rot_vel[1] = data.angular_velocity.y
        self.rot_vel[2] = data.angular_velocity.z

    def set_rot_target(self, r, p, y):
        self.rot_target = quaternion_from_euler(r,p,y)
        

    def run(self, dt):
        
        rpy_vel_targets = self.qp_attitude_controller.get_angular_setpoint(self.rot_target, self.rot_quat)
        
        for i in range(3):
            self.rot_pid[i].set_state(self.rot_vel[i])
            self.rot_pid[i].update(rpy_vel_targets[i], dt)

        self.thrust_list[0] = self.rot_pid[2].get_output_ff(KF_ANGULAR, rpy_vel_targets[2])
        self.thrust_list[1] = -self.rot_pid[2].get_output_ff(KF_ANGULAR, rpy_vel_targets[2])
        self.thrust_list[2] = self.rot_pid[2].get_output_ff(KF_ANGULAR, rpy_vel_targets[2])
        self.thrust_list[3] = -self.rot_pid[2].get_output_ff(KF_ANGULAR, rpy_vel_targets[2])
        self.thrust_list[4] = -self.rot_pid[1].get_output_ff(KF_ANGULAR, rpy_vel_targets[1]) + self.rot_pid[0].get_output_ff(KF_ANGULAR, rpy_vel_targets[0])
        self.thrust_list[5] = self.rot_pid[1].get_output_ff(KF_ANGULAR, rpy_vel_targets[1]) + self.rot_pid[0].get_output_ff(KF_ANGULAR, rpy_vel_targets[0])
        self.thrust_list[6] = -self.rot_pid[1].get_output_ff(KF_ANGULAR, rpy_vel_targets[1]) -  self.rot_pid[0].get_output_ff(KF_ANGULAR, rpy_vel_targets[0])
        self.thrust_list[7] = self.rot_pid[1].get_output_ff(KF_ANGULAR, rpy_vel_targets[1]) - self.rot_pid[0].get_output_ff(KF_ANGULAR, rpy_vel_targets[0])


    def enter(self):
        pass

    def exit(self):
        pass

    def get_thrust_list(self):
        return self.thrust_list

