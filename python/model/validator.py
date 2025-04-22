from view.logger import Logger
from model.model import Model
from enums.change import Change
from .validation import Validation
from .helper import Helper
import os, sys

class Validator:
    def __init__(self, model: Model):
        self.model = model
        self.model.add_property_change_listener(self.listener)
        
    def match_commands(self, command: str):
        match command:
            case "clear" | "cls":
                if os.name == "nt": 
                    os.system("cls")
                else: 
                    os.system("clear")
            case "help":
                self.model.command = "help", {}
                return True
            case "exit": 
                sys.exit(0)
                return True
            case "save":
                self.model.save = not self.model.save
                self.model.command = False
                return self.model.prompt_and_check()
            case "debug":
                self.model.debug = not self.model.debug
                self.model.command = False
                return self.model.prompt_and_check()
            case "show": 
                self.model.command = "show", {}
                return True
            case "next": 
                if not self.model.results_preview:
                    Logger.warning("Nothing searched, use search command")
                    return self.model.prompt_and_check()
                
                self.model.command = "next", {}
            case _:
                raise ValueError("Not a valid command")

    def match_flag_commands(self, command: str):
        match command:
            case "search": 
                validators = {
                    "pid": Validation.validate_pid,
                    "name": Validation.validate_name,
                }
            
                flags = Helper.validate_and_update_values(self.model.command, validators)
                
                validators = {
                    "geo": lambda x: x,
                    "gender": Validation.validate_gender,
                    "min": lambda x: Validation.validate_age(x, is_min=True),
                    "max": lambda x: Validation.validate_age(x, is_min=False),
                }
            
                Helper.check_and_update_flags(self.model.command, validators)
                        
                """
                flags_required = [flags['name'], flags['geo'], flags['pid']]
                true_count = sum(bool(value) for value in flags_required)
                
                if true_count > 2:
                    raise ValueError("Too many parameters used")
                
                if not true_count:
                    raise ValueError("No parameters given")
                
                if not flags['geo']:
                    if true_count == 2:
                        raise ValueError("Used two purple parameters")
                """
            case "lookup": 
                validators = {
                    "phone": lambda x: Validation.validate_phone(x),
                    "index": lambda x: Validation.validate_index(x, len(self.model.results_preview)),
                    "pid": lambda x: Validation.validate_pid(x),
                }
                
                Helper.check_and_update_flags(self.model.command, validators)
            case _:
                raise ValueError("Not a valid command")

    def valid_command(self):
        try:
            self.match_command(self.model.command)
            self.match_flag_commands(Helper.check_for_flags(self.model.command))
        except ValueError as e:
            Logger.warning(e)
            return self.model.prompt_and_check()
    
    def listener(self, value, old, new):
        match value:
            case "VALIDATE":
                if self.valid_command():
                    self.model.fire_property_change(Change.EXECUTE)
            case _:
                return
            
"""
    def able_to_display(self):
        try:
            flags = {}

            split = self.model.command.split(" ")
            if not len(split) == 2:
                raise ValueError("Not enough arguments given")
            
            value = split[1]
            if not value.isdigit():
                raise ValueError("Invalid selection, not a positive integer")

            if int(value) >= len(self.model.results):
                raise ValueError("Selection not in list")
            
            id = self.model.results_preview[value].id
            found = False
            for user in self.model.results_preview:
                if id == user.id: found = True
            if not found:
                raise ValueError("Person hasn't been looked up")

            flags['value'] = value
            
            self.update_command("display", flags)
            return True
        except ValueError as e:
            Logger.warning(e)
            return self.model.prompt_and_check()
"""