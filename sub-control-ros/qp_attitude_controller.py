import numpy as np

class QuaternionAttitudeController():
    
    def __init__(self, kP):
        self.kP = kP
        
    
    def quaternion_multiply(self, quaternion1, quaternion0):
        x0, y0, z0, w0 = quaternion0
        x1, y1, z1, w1 = quaternion1
        return np.array([x1 * w0 + y1 * z0 - z1 * y0 + w1 * x0,
                        -x1 * z0 + y1 * w0 + z1 * x0 + w1 * y0,
                        x1 * y0 - y1 * x0 + z1 * w0 + w1 * z0,
                        -x1 * x0 - y1 * y0 - z1 * z0 + w1 * w0], dtype=np.float64)
    
    def get_error_quat(self, setpoint, current):
        current_conj = np.array(current) * np.array([-1,-1,-1,1])
        setpoint = np.array(setpoint)
        
        error_quat = self.quaternion_multiply(current_conj, setpoint) #this is the error quaternion
        #check that the error quaternion is in the correct hemisphere
        
        if error_quat[3] < 0:
            error_quat = -error_quat
            
        return error_quat
    
    def get_angular_setpoint(self, setpoint, current):
        return 2*self.kP*self.get_error_quat(setpoint, current)[0:3]
        
        