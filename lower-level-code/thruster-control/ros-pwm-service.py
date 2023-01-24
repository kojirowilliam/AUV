#!/usr/bin/env python
import board
import rospy
import busio
import numpy as np
from pwm_to_thrust import *
from std_msgs.msg import String

# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685

joy = XboxController()

i2c_bus = busio.I2C(board.SCL, board.SDA)

pca = PCA9685(i2c_bus)
pca.frequency = 333.333

#pca duty cycle is 16 bits

thrust_controller = PWM_To_Thrust(pca.frequency)

MAX_THRUST = 3.0

def callback(data):
    val1 = data.data
    pca.channels[1].duty_cycle = int(thrust_controller.get_duty_cycle(20, MAX_THRUST*val1))

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('pwm-service', anonymous=False)
True
    rospy.Subscriber('power_output', String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()