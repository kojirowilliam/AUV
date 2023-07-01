class fsm_state():
    def __init__(self):
        pass

    def get_name(self):
        return self.name

    def enter(self):
        pass
    def run(self, dt):
         raise NotImplementedError("run function not implemented")
    def exit(self):
        pass

    def set_rot_target(self, r, p, y):
        pass

    def get_thrust_list(self):
        pass