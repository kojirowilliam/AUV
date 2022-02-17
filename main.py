# from board import SCL, SDA
# import busio
# from adafruit_pca9685 from PCA9685
import csv
import pandas as pd


def rpm2pwn(rpm, voltage):
    '''
    Converts the desired RPM to a PWN signal depending on the voltage.

    :parameters:
    rpm : The rpm that you want the motor to move at
    voltage : The current voltage supplied to the motor

    :return:
    pwn : The PWN signal in microseconds
    '''
    if voltage == 18:
        parameters = ['PWM', 'RPM', 'Current', 'Voltage', 'Power', 'Force', 'Efficiency']
        data = pd.read_csv("18voltage.csv", usecols=parameters)
        rpmData = [int(speed) for speed in data['RPM']]
        pwnData = [int(pwn) for pwn in data['PWM']]
        absolute_difference_function = lambda list_value : abs(list_value - rpm)
        closest_rpm = min(rpmData, key=absolute_difference_function)
        rpm_index = rpmData.index(closest_rpm)
        pwn = int(pwnData[rpm_index])
        return pwn
    raise Exception("Voltage of Unknown Type Given")


def i2cToPwn(motor, value, valueType, SCL, SDA):
    '''
    Sends i2c data to the Adafruit PCA 9685 board, which generates a PWM signal to the motors.

    :parameter:
    motor : The motor that you want to utilize (0-7)
    value : The RPM or thrust speed that you want the motor to move
    valueType : The type of 'value' ('rpm' or 'thrust')
    SCL : Connection to the SCL data on the Jetson
    SDA : Connection to the SDA data on the Jetson
    '''
    #TODO:WILL Assuming the voltage will be at 18
    FREQUENCY = 400 # The max update rate of the Blue Robotics Basic ESC
    # i2c_bus = busio.I2C(SCL, SDA)
    # pca = PCA9685(i2c_bus)
    if 0 > motor or motor > 7:
        raise TypeError("Must declare a motor between 0 and 7!")
    #TODO:WILL Create other tests

    if valueType == "rpm":
        #TODO WILL You were trying to figure out the duty cycle
        # 2**16 * max_pulsewidth in microseconds
        duty_cycle = rpm2pwn(value, 18) # 18 stands for voltage

    else:
        duty_cycle =
    pca.frequency = FREQUENCY
    pca.channels[motor].duty_cycle = dut




if __name__ == '__main__':
    rpm2pwn(3600, 18)




    # pca.frequency = 60 #Not really sure what this does
    # pca.channels[0].duty_cycle = 0x7FFF #Not really sure what this does