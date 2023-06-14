import keyboard
from fsm_state import fsm_state

class fsm_basic(fsm_state):
    def __init__(self):
       self.name = 'basic'


    def get_thrust_list(self):
        list = [0,0,0,0,0,0,0,0]
        for i in range(8):
            if keyboard.is_pressed(str(i+1)):
                list[i] = 100
        
        return list
    
