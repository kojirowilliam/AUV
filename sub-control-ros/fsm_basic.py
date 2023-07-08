#import keyboard
from fsm_state import fsm_state

class fsm_basic(fsm_state):
    def __init__(self):
       self.name = 'basic'

    # 1 bl, 2 br, 3 fr, 4 fl
    # 7 bl, 8 br, 6 fr, 5 fl vert

    def run(self, dt):
        pass

    def get_thrust_list(self):
        list = [0,0,0,0,0,0,0,0]
        #for i in range(8):
            #if keyboard.is_pressed(str(i+1)):
            #    list[i] = 100
        
        return list
    
