from abc import ABC, abstractmethod

class fsm_state(ABC):
    def get_name(self):
        return self.name

    @abstractmethod
    def enter(self):
        pass

    @abstractmethod
    def run(self, dt):
        pass
    
    @abstractmethod
    def exit(self):
        pass

    @abstractmethod
    def set_rot_target(self, r, p, y):
        pass

    @abstractmethod
    def get_thrust_list(self):
        pass