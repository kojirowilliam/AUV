from fsm_basic import fsm_basic
from fsm_pcontrol import fsm_pcontrol

class fsm(): 
    def __init__(self):
        self.state_list = [fsm_basic(), fsm_pcontrol()]
        self.current_state = self.state_list[0]
    
    def get_next_state(self):
        if self.current_state.get_name() == 'passive':
            return 'pcontrol'
        
        if self.current_state.get_name() == 'pcontrol':
            return 'passive'
        
    def get_state(self):
        return self.current_state