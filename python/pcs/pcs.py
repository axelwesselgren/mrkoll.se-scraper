from enums.change import Change

class PropertyChangeSupport:
    def __init__(self):
        self.listeners = []
        
    def add_property_change_listener(self, listener):
        if listener not in self.listeners:
            self.listeners.append(listener)

    def remove_property_change_listener(self, listener):
        if listener in self.listeners:
            self.listeners.remove(listener)

    def fire_property_change(self, change: Change, old_value, new_value):
        for listener in self.listeners:
            listener(change.value, old_value, new_value) 