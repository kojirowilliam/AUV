# from board import SCL, SDA
# import busio
# from adafruit_pca9685 from PCA9685
import pandas as pd

def pwmToDutyCycle(pwm, frequency):
    '''
    Converts 'pwm' to a duty cycle
    :parameters:
    pwm: A pwm value in microseconds
    frequency: The frequency the PCA 9685 is running at
    :return:
    dutyCycle: The duty cycle of the PWM signal
    '''
    duration = 1/frequency
    duration *= 10^6
    dutyCycle = duration*pwm
    return dutyCycle

def findNearestInt(lis, integer):
    '''
    Returns the index of the number closest to 'integer' in the list 'lis'
    :param lis: The list that you want to find the closest number to 'integer' in
    :param integer: The number you want to find in 'lis'
    :return:
    int_index: The index of the integer in 'lis' closest to 'integer'
    '''
    absolute_difference_function = lambda list_value: abs(list_value - integer)
    closest_int = min(lis, key=absolute_difference_function)
    int_index = lis.index(closest_int)
    return int_index


def getMotorData(valueType, voltage):
    '''
    Returns a list of the PWM data and correlating RPM data from the voltage provided in the
    motor documentation
    :parameters:
    valueType: The type of value. Either 'thrust' or 'rpm'
    voltage: The voltage the motor is running at
    :return:
    motorData: A list of the 'valueType' correlating with the pwmData list
    pwmData: A list of the possible PWM values in microseconds for the motor

    '''
    parameters = ['PWM', 'RPM', 'Current', 'Voltage', 'Power', 'Force', 'Efficiency']

    if voltage == 18:
        data = pd.read_csv("18voltage.csv", usecols=parameters)
        pwmData = [int(pwm) for pwm in data['PWM']]
        if valueType == 'rpm':
            motorData = [int(speed) for speed in data['RPM']]
        else:
            motorData = [int(force) for force in data['Force']]
        return motorData, pwmData

    raise NotImplementedError("Inputted Voltage is Not Implemented!")


def rpmToPwm(rpm, voltage):
    '''
    Converts the desired RPM to a pwm signal depending on the voltage.

    :parameters:
    rpm : The rpm that you want the motor to move at
    voltage : The current voltage supplied to the motor

    :return:
    pwm : The pwm signal in microseconds
    '''
    rpmData, pwmData = getMotorData('rpm', voltage)
    rpm_index = findNearestInt(rpmData, rpm)
    pwm = int(pwmData[rpm_index])
    return pwm


def thrustToPwm(thrust, voltage):
    '''
    Converts the desired thrust to a pwm signal depending on the voltage.

    :parameters:
    thrust : The amount of thrust that you want the motor to push
    voltage : The current voltage supplied to the motor

    :return:
    pwm : The pwm signal in microseconds
    '''
    thrustData, pwmData = getMotorData('thrust', voltage)
    thrust_index = findNearestInt(thrustData, thrust)
    pwm = int(pwmData[thrust_index])
    return pwm


def spinMotor(motor, value, valueType, SCL, SDA):
    '''
    Sends i2c data to the Adafruit PCA 9685 board, which generates a PWM signal to the motors.

    :parameter:
    motor : The motor that you want to utilize (0-7)
    value : The RPM or thrust speed that you want the motor to move
    valueType : The type of 'value' ('rpm' or 'thrust')
    SCL : Connection to the SCL data on the Jetson
    SDA : Connection to the SDA data on the Jetson
    '''
    FREQUENCY = 400 # The max update rate of the Blue Robotics Basic ESC
    # i2c_bus = busio.I2C(SCL, SDA)
    # pca = PCA9685(i2c_bus)
    if 0 > motor or motor > 7:
        raise TypeError("Must declare a motor between 0 and 7!")
    #TODO:WILL Create other tests

    if valueType == "rpm":
        duty_cycle = pwmToDutyCycle(rpmToPwm(value, 18), 400) # 18 stands for voltage

    else:
        duty_cycle = pwmToDutyCycle(thrustToPwm(value, 18), 400) # 18 stands for voltage

    pca.frequency = FREQUENCY
    pca.channels[motor].duty_cycle = duty_cycle # Might need to be in hexadecimal


if __name__ == '__main__':
    rpmToPwm(3600, 18)



