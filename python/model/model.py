from pcs.pcs import PropertyChangeSupport
from enums.change import Change
from colorama import Fore, Style

class Model:
    def __init__(self):
        self.session = None
        self.search = None

        self.command = None

        self.current_page = 1

        self.results_preview = []
        self.results = []

        self.save = False
        self.debug = False

        self.pcs = PropertyChangeSupport()

    def prompt_and_check(self):
        self.command = input(f"{Fore.CYAN}[PROMPT]{Style.RESET_ALL} Command > ")
        self.fire_property_change(Change.VALIDATE)

    def fire_property_change(self, change: Change, old=None, new=None):
        self.pcs.fire_property_change(change, old, new)

    def add_property_change_listener(self, listener):
        self.pcs.add_property_change_listener(listener)

    def remove_property_change_listener(self, listener):
        self.pcs.remove_property_change_listener(listener)