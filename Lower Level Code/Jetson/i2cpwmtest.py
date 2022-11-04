import board
import busio
import numpy as np
from pwm_to_thrust import *

# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685

joy = XboxController()

i2c_bus = busio.I2C(board.SCL, board.SDA)

pca = PCA9685(i2c_bus)
pca.frequency = 333.333

#pca duty cycle is 16 bits

thrust_controller = PWM_To_Thrust(pca.frequency)

MAX_THRUST = 3.0

while True:
    joy_left_y = joy.read()[1]
    pca.channels[1].duty_cycle = int(65536*(joy_left_y+1)/2)
    
    #int(thrust_controller.get_duty_cycle(20, MAX_THRUST*joy_left_y))