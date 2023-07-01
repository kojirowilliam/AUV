from fsm_state import fsm_state
from pid_control import pid

class fsm_pcontrol(fsm_state):
    def __init__(self):
        self.name = 'pcontrol'
        # 0 is x, 1 is y, 2 is z
        self.rot_pid = [None]*3
        self.rot_pid[0] = pid(1,0,0)
        self.rot_pid[1] = pid(1,0,0)
        self.rot_pid[2] = pid(1,0,0)

        self.pos_pid = pid(0,0,0)



    def enter(self):
        pass

    def get_thrust_list(self):
        return [0,0,0,0,0,0,0,0]

