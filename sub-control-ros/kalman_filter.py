import numpy as np

class KalmanFilter():
    
    # A: state transition matrix
    # B: control input matrix
    # P: error covariance matrix
    # H: measurement matrix
    # X: state vector
    def __init__(self, A, B, P):
        self.X_ = np.zeros((A.shape[0], 1))
        self.A_ = A
        self.B_ = B
        self.P_ = P
        
    # H: measurement matrix
    # U: control input
    # Z: measurement
    # Q: process noise covariance
    # R: measurement noise covariance
    # dt: time step
    def update(self, H, U, Z, Q, R, dt):
        
        
        
        X_ = self.A_ @ self.X_ + self.B_ + U #project the state estimate
        P_ = (self.A_ @ self.P_ @ self.A_.transpose()) + Q #project the error covariance
        K = P_ @ self.H_.transpose()@np.linalg.inv(self.H_@P_@self.H_.transpose()+R) #compute the Kalman gain
        X_ = X_ + K@(Z - self.H_@X_) #update the estimate via z
        P_ = (np.eye(self.H_.shape[0]) - K@self.H_)@P_
        
        self.X_ = X_
        self.P_ = P_
        
        

# create transition matrix for a xyzrpy constant acceleration model
A = np.array([[1, 0, 0, 0, 0, 0, dt, 0, 0, 0, 0, 0, 0.5*dt**2, 0, 0, 0, 0, 0],
              [0, 1, 0, 0, 0, 0, 0, dt, 0, 0, 0, 0, 0, 0.5*dt**2, 0, 0, 0, 0],
              [0, 0, 1, 0, 0, 0, 0, 0, dt, 0, 0, 0, 0, 0, 0.5*dt**2, 0, 0, 0],
              [0, 0, 0, 1, 0, 0, 0, 0, 0, dt, 0, 0, 0, 0, 0, 0.5*dt**2, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, dt, 0, 0, 0, 0, 0, 0.5*dt**2, 0],
              [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, dt, 0, 0, 0, 0, 0, 0.5*dt**2],
              [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, dt, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, dt, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, dt, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, dt, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, dt, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, dt],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]])

# initialize P 
P = np.eye(A.shape[0])
# initialize Q
Q = np.eye(A.shape[0])*0.1

# initialize R for the imu
R = np.eye(6)*0.1

# initialize R for the dvl
R = np.eye(3)*0.1

# initialize H for the imu

H_imu = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]])

# initialize H for the DVL

H_dvl = np.array([[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0 ,0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0 ,0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0 ,0, 0, 0, 0, 0, 0, 0]])

              
        
