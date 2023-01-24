class pid():
    def __init__(self, kP, kI, kD, integral_bound = 1000):
        self.kP = kP
        self.kI = kI
        self.kD = kD
        self.value = 0
        self.last_error = 0
        self.integral = 0
        self.integral = integral_bound
    
    def get_output(self, target, dt):
        error = target - self.value
        integral = integral + error*dt
        if integral+error*dt < self.integral_bound or integral > -self.integral_bound:
            integral = integral + error*dt
        derivative = (error - self.last_error)*dt
        self.last_error = error
        return self.kP*error+self.kI*integral+self.kD*derivative
    
    def reset(self):
        self.integral = 0
        self.last_error = 0
        self.value = 0
    
