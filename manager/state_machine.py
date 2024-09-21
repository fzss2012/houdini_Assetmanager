class StateManager:
    _instance = None  # 单例实例存储
    _observers = []  # 观察者列表

    # @classmethod
    # def get_instance(cls):
    #     if cls._instance is None:
    #         cls._instance = cls()
    #     return cls._instance
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StateManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.current_state = "idle"
        self.states = {
            "idle": {"start_drawing": "drawing"},
            "drawing": {"stop_drawing": "idle"}
        }
        self.state_actions = {
            "drawing": {
                "enter": self.prepare_drawing_tools,
                "exit": self.cleanup_drawing_tools
            }
        }

    def transition(self, action):
        if action in self.states[self.current_state]:
            new_state = self.states[self.current_state][action]
            self.exit_state(self.current_state)
            self.current_state = new_state
            self.enter_state(self.current_state)
            self.notify_observers()  # 通知观察者状态已改变
            return True
        return False

    def enter_state(self, state):
        if state in self.state_actions and "enter" in self.state_actions[state]:
            self.state_actions[state]["enter"]()

    def exit_state(self, state):
        if state in self.state_actions and "exit" in self.state_actions[state]:
            self.state_actions[state]["exit"]()

    def prepare_drawing_tools(self):
        return True

    def cleanup_drawing_tools(self):
        return True

    def get_state(self):
        return self.current_state

    # 添加观察者
    def register_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            if hasattr(observer, 'update'):
                observer.update(self.current_state)
            else:
                print(f"Error: Registered observer {observer} does not have an 'update' method")



class ConcreteObserver:
    def update(self, state):
        return True