import rospy
import numpy
from sensor_msgs.msg import Imu
from tf.transformations import quaternion_from_euler, euler_from_quaternion
from qp_attitude_controller import QuaternionAttitudeController
from fsm_state import fsm_state
from pid_control import pid
from kalman_filter import kalmanfilter


IMU_TOPIC = "mantaray/imu"
KF_ANGULAR = 120

# initialize H for the imu

H_IMU = np.array([  [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # roll
                    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # pitch
                    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # yaw
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], # roll rate
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], # pitch rate
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], # yaw rate
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # x accel
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], # y accel
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]])# z accel

U = np.eye(18)*0.1


# initialize Q
Q = np.eye(18)*0.1


class fsm_pcontrol(fsm_state):
    def __init__(self):
        self.name = 'pcontrol'
        self.kf = kalmanfilter()
        self.last_imu_timestamp = 0

        # 0 is x, 1 is y, 2 is z
        self.rot_pid = [None]*3
        self.rot_pid[0] = pid(20,0,0)
        self.rot_pid[1] = pid(20,0,0)
        self.rot_pid[2] = pid(20,0,0) #150, 0 ,0
        
        self.qp_attitude_controller = QuaternionAttitudeController(2)

        self.rot_target = [0,0,0,0]

        self.pos_pid = pid(0,0,0)
        self.thrust_list = [0,0,0,0,0,0,0,0]
        self.rot_quat = [0,0,0,0]

        self.imu_listener = rospy.Subscriber(IMU_TOPIC, Imu, self.imu_callback)

    def imu_callback(self, data):

        if last_imu_timestamp > 0:
            dt = data.header.sec - last_imu_timestamp
        last_imu_timestamp = data.header.sec


        imu_quat[0] = data.orientation.x
        imu_quat[1] = data.orientation.y
        imu_quat[2] = data.orientation.z
        imu_quat[3] = data.orientation.w
        
        imu_euler = euler_from_quaternion(rot_quat)

        Z = [imu_euler[0],
             imu_euler[1],
             imu_euler[2],
             data.angular_velocity.x,
             data.angular_velocity.y,
             data.angular_velocity.z,
             data.linear_acceleration.x,
             data.linear_acceleration.y,
             data.linear_acceleration.z]

        ori_cov = data.orientation_covariance
        angvel_cov = data.angular_velocity_covariance
        linacc_cov = data.linear_acceleration_covariance

        if ori_cov[0][0] = -1:
            ori_cov = np.zeros(9)

        R_IMU = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,ori_cov[0],ori_cov[1],ori_cov[2],0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,ori_cov[3],ori_cov[4],ori_cov[5],0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,ori_cov[6],ori_cov[7],ori_cov[8],0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])

        self.kf.update(H_IMU, U, Z, Q, R_IMU, dt)

    def set_rot_target(self, r, p, y):
        self.rot_target = quaternion_from_euler(r,p,y)
        

    def run(self, dt):
        
        rot_vel = self.kf.get_rpy_vel()

        rpy_vel_targets = self.qp_attitude_controller.get_angular_setpoint(self.rot_target, self.rot_quat)
        
        
        for i in range(3):
            self.rot_pid[i].set_state(rot_vel[i])
            self.rot_pid[i].update(rpy_vel_targets[i], dt)

        self.thrust_list[0] = self.rot_pid[2].get_output_ff(KF_ANGULAR, rpy_vel_targets[2])
        self.thrust_list[1] = -self.rot_pid[2].get_output_ff(KF_ANGULAR, rpy_vel_targets[2])
        self.thrust_list[2] = self.rot_pid[2].get_output_ff(KF_ANGULAR, rpy_vel_targets[2])
        self.thrust_list[3] = -self.rot_pid[2].get_output_ff(KF_ANGULAR, rpy_vel_targets[2])
        self.thrust_list[4] = -self.rot_pid[1].get_output_ff(KF_ANGULAR, rpy_vel_targets[1]) - self.rot_pid[0].get_output_ff(KF_ANGULAR, rpy_vel_targets[0])
        self.thrust_list[5] = self.rot_pid[1].get_output_ff(KF_ANGULAR, rpy_vel_targets[1]) - self.rot_pid[0].get_output_ff(KF_ANGULAR, rpy_vel_targets[0])
        self.thrust_list[6] = -self.rot_pid[1].get_output_ff(KF_ANGULAR, rpy_vel_targets[1]) +  self.rot_pid[0].get_output_ff(KF_ANGULAR, rpy_vel_targets[0])
        self.thrust_list[7] = self.rot_pid[1].get_output_ff(KF_ANGULAR, rpy_vel_targets[1]) + self.rot_pid[0].get_output_ff(KF_ANGULAR, rpy_vel_targets[0])


    def enter(self):
        pass

    def exit(self):
        pass

    def get_thrust_list(self):
        return self.thrust_list

