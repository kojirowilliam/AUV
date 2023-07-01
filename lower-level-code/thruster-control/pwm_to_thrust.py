from ctypes.wintypes import PWIN32_FIND_DATAA
import pandas
from scipy import interpolate
import matplotlib.pyplot as plt
import numpy as np
from xbox_controller import XboxController

class PWM_To_Thrust:
    def __init__(self, pwm_freq):
        self.pwm_freq = pwm_freq
        self.data_file = "T200 Data.csv"
        self.data = [pandas.read_csv(self.data_file,  header=0, usecols=["x1neg", "y1neg"]),
                     pandas.read_csv(self.data_file,  header=0, usecols=["x1pos", "y1pos"]),
                     pandas.read_csv(self.data_file,  header=0, usecols=["x2neg", "y2neg"]),
                     pandas.read_csv(self.data_file,  header=0, usecols=["x2pos", "y2pos"]),
                     pandas.read_csv(self.data_file,  header=0, usecols=["x3neg", "y3neg"]),
                     pandas.read_csv(self.data_file,  header=0, usecols=["x3pos", "y3pos"]),
                     pandas.read_csv(self.data_file,  header=0, usecols=["x4neg", "y4neg"]),
                     pandas.read_csv(self.data_file,  header=0, usecols=["x4pos", "y4pos"]),
                     pandas.read_csv(self.data_file,  header=0, usecols=["x5neg", "y5neg"]),
                     pandas.read_csv(self.data_file,  header=0, usecols=["x5pos", "y5pos"]),
                     pandas.read_csv(self.data_file,  header=0, usecols=["x6neg", "y6neg"]),
                     pandas.read_csv(self.data_file,  header=0, usecols=["x6pos", "y6pos"])]
        self.interp_functions = list()
        for i in range(6):
            x1 = self.data[2*i][f'x{i+1}neg'].array
            y1 = self.data[2*i][f'y{i+1}neg'].array
            x2 = self.data[2*i+1][f'x{i+1}pos'].array
            y2 = self.data[2*i+1][f'y{i+1}pos'].array
            self.interp_functions.append([interpolate.interp1d(x1[~np.isnan(x1)], y1[~np.isnan(y1)], kind='cubic', bounds_error=False, fill_value=1500), 
                                interpolate.interp1d(x2[~np.isnan(x2)], y2[~np.isnan(y2)], kind='cubic', bounds_error=False, fill_value=1500)]) 
            
        
    #freq of cycle (hz)
    #returns a 16 bit number
    def microseconds_to_int16(self, time, freq):
        return time*freq*65536/1000000
    
    #assuming volts is between a and b
    def voltage_lin_approx(self, a, b, volts, val):
        if val > 0:
            is_positive = 1
        elif val < 0:
            is_positive = 0
        else:
            return 1500
            
        y1 = self.interp_functions[b][is_positive](val)
        y0 = self.interp_functions[a][is_positive](val)
        d = y1 - y0
        return d*(volts-(2*a+10))/2+y0
            
    def get_duty_cycle(self, voltage, thrust):
        if 10 <= voltage <= 12:
            res = self.voltage_lin_approx(0, 1, voltage, thrust)
        elif 12 < voltage <= 14:
            res = self.voltage_lin_approx(1, 2, voltage, thrust)
        elif 14 < voltage <= 16:
            res = self.voltage_lin_approx(2, 3, voltage, thrust)
        elif 16 < voltage <= 18:
            res = self.voltage_lin_approx(3, 4, voltage, thrust)
        elif 18 < voltage <= 20:
            res = self.voltage_lin_approx(4, 5, voltage, thrust)
        else:
            res = 1500
        
        return round(self.microseconds_to_int16(res, self.pwm_freq))