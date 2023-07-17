import os
import subprocess
import pandas as pd

class Thruster():
    '''
    With these thrusters, I want the input to be how much thrust (kg f) the user wants and
    the output to depend whether the Thruster is used in the sim (output will be a FloatStamped)
    or in real life (output will be a PWM or I2C signal).
    '''
    def __init__(self, saturation, voltage=12, output="pwm"):
        '''
        Parameters
        -----
        saturation : int/float
            The max thrust of the motor
        voltage : int
            How many volts is supplied to the 
        output : "pwm", "i2c", or "both"
            The type of output you want
        '''
        GOOD_VOLTS = [10,12,14,16,18,20]
        self.saturation = saturation
        self.current_thrust = 0
        self.voltage = [volt for volt in GOOD_VOLTS if voltage-volt<=1][0]
        self.voltage = str(self.voltage)
        self.output = output
        self.pwm = None
        self.i2c = None
        
        temp = subprocess.Popen(["rospack", "find", "mantaray_control"], stdout=subprocess.PIPE)
        temp_output = temp.communicate()[0]
        temp_output = str(temp_output)[0:-1]
        # temp_output = str(temp_output)[2:-3]
        file_path = temp_output
        iodata_path = os.path.join(file_path, "data","t200_data", self.voltage+" V", "force_pwm.csv")

        self.iodata = pd.read_csv(iodata_path)

        df_stop_pwm = self.iodata.iloc[(self.iodata[' Force (Kg f)']-self.current_thrust).abs().argsort()[:1]]
        self.update_pwm()

    def set_thrust(self, thrust):
        self.current_thrust = max(min(thrust, self.saturation), -self.saturation)
        if self.output == "pwm":
            self.update_pwm()
        elif self.output == "i2c":
            self.update_i2c()
        else:
            # If unknown or "both", update both for resiliency
            self.update_pwm()
            self.update_i2c()

    def get_thrust(self):
        return self.current_thrust
    
    def add_thrust(self, thrust):
        self.set_thrust(self.current_thrust+thrust)

    def update_voltage(self, volt):
        # Use in case of dynamic voltage. Can be useful for long-term operations
        pass

    def reset(self):
        self.current_thrust = 0
        if self.output == "pwm":
            self.update_pwm()
        elif self.output == "i2c":
            self.update_i2c()

    def update_pwm(self):
        # This calculates the approximate PWM signal necessary to get the needed thrust
        df_closest = self.iodata.iloc[(self.iodata[' Force (Kg f)']-self.current_thrust).abs().argsort()[:1]]
        # df_closest = self.iodata.iloc[(self.iodata[' Force (Kg f)']-self.current_thrust).abs().argsort()[:2]] # returns the 2 closest pwm values
        self.pwm = df_closest.values[0][2]

    def update_i2c(self):
        # This calculates the approximate PWM signal necessary to get the needed thrust
        pass

    def get_pwm(self):
        # This is in microseconds
        return self.pwm
    
    def get_i2c(self):
        # This utilizes the pca9685 library
        pass


# class SimThruster(Thruster):
#     def __init__(self, saturation):
#         super().__init__(saturation)


# class RealThruster(Thruster):
#     def __init__(self, saturation):
#         super().__init__(saturation)

# if __name__ == "__main__":
#     sat = 3
#     test_thruster = Thruster(sat)
#     print(test_thruster.get_pwm())