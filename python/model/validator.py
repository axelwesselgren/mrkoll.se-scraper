from view.console import print_warning
from model.model import Model
from enums.change import Change
import re, os, sys

class Validator:
    pid_with_4 = r'^(19|20)?[0-9]{2}[- ]?((0[0-9])|(10|11|12))[- ]?(([0-2][0-9])|(3[0-1])|(([7-8][0-9])|(6[1-9])|(9[0-1])))[- ]?[0-9]{4}$'
    swedish_phone = r'^(\+46|0)(\s?-?\d{1,4})(\s?-?\d{2,3})(\s?-?\d{2,3})(\s?-?\d{2})$'
    swedish_name = r'^[a-zA-ZåäöÅÄÖ ]+$'
    pid = r'^\d{6}$|^\d{8}$|^(?:\d{2}|\d{4})\d{2}\d{2}\d{2}$'

    def __init__(self, model: Model):
        self.model = model
        self.model.add_property_change_listener(self.listener)

    def valid_command(self):
        match self.model.command:
            case "clear" | "cls":
                if os.name == "nt": 
                    os.system("cls")
                else: 
                    os.system("clear")
                # return repl()
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
                return self.able_to_next()
        
        cmd = self.model.command.split("--")[0].strip()
        dash_index = self.model.command.find("-")
        if dash_index == -1:
            cmd = self.model.command.split(" ")[0]

        match cmd:
            case "search": 
                return self.valid_search()
            case "lookup": 
                return self.valid_lookup()
            case _:
                print_warning("Not a valid command")
                return self.model.prompt_and_check()

    def valid_lookup(self):
        flags = {}

        flags['phone'] = ""
        flags['pid'] = ""
        flags['index'] = -1

        split = self.model.command.split("--")
        for i in range(1, len(split), 1):
            split_space = split[i].split(" ")
            if (len(split_space) <= 1):
                print_warning(f"No value given to the flag: {split[0]}")
                return self.model.prompt_and_check()

            value = " ".join(split_space[1:]).strip()
            match split_space[0]:
                case "phone":
                    if not re.match(self.swedish_phone, value):
                        print_warning("Not a valid Swedish phone number")
                        return self.model.prompt_and_check()
                    flags['phone'] = value
                case "index":
                    if not value.isdigit():
                        print_warning("Invalid selection, not a positive integer")
                        return self.model.prompt_and_check()

                    if int(value) >= len(self.model.results_preview):
                        print_warning("Selection not in list")
                        return self.model.prompt_and_check()
                    
                    flags['index'] = int(value)
                case "pid":
                    if not re.match(self.pid_with_4, value):
                        print_warning("Not a valid Swedish PID")
                        return self.model.prompt_and_check()
                    flags['pid'] = value.replace(" ", "").replace("-", "")
        self.model.command = "help", flags
        return True

    def able_to_display(self):
        flags = {}

        split = self.model.command.split(" ")
        if not len(split) == 2:
            print_warning("Too few | many arguments")
            return self.model.prompt_and_check()
        
        value = split[1]
        if not value.isdigit():
            print_warning("Invalid selection, not a positive integer")
            return self.model.prompt_and_check()

        if int(value) >= len(self.model.results):
            print_warning("Selection not in list")
            return self.model.prompt_and_check()
        
        id = self.model.results_preview[value].id
        found = False
        for user in self.model.results_preview:
            if id == user.id: found = True
        if not found:
            print_warning("Person hasn't been looked up")
            return self.model.prompt_and_check()

        flags['value'] = value
        self.model.command = "display", flags
        return True

    def able_to_next(self):
        if not self.model.results_preview:
            print_warning("Nothing searched, use search command")
            return self.model.prompt_and_check()
        self.model.command = "next", {}
        return True

    def valid_search(self):
        flags = {}

        flags['gender'] = 'a'
        flags['geo'] = ""
        flags['min'] = 16
        flags['max'] = 120
        flags['pid'] = ""
        flags['name'] = ""

        dash_index = self.model.command.find("-")
        if dash_index == -1:
            id = " ".join(self.model.command.split(" ")[1:])
            name_bool = re.match(self.swedish_name, id)
            pid_bool = re.match(self.pid, id)
            if not name_bool and not pid_bool:
                print_warning("Not a valid name or PID")
                return self.model.prompt_and_check()
            if pid_bool:
                if id[0:2] == "20" or id[0:2] == "19":
                    if len(id) == 6:
                        print_warning("Not a valid PID")
                        return self.model.prompt_and_check()
                flags['pid'] = id
            if name_bool: flags['name'] = id
    
        split = self.model.command.split("--")
        for i in range(1, len(split), 1):
            split_space = split[i].split(" ")
            if (len(split_space) <= 1):
                print_warning(f"No value given to the flag: {split[0]}")
                return self.model.prompt_and_check()

            value = " ".join(split_space[1:]).strip()
            match split_space[0]:
                case "geo":
                    flags['geo'] = value
                case "gender":
                    if not value == "m" and not value == "w" and not value == "a":
                        print_warning(f"Not a valid gender: {value}")
                        return self.model.prompt_and_check()
                    flags['gender'] = value
                case "min":
                    if not value.isdigit():
                        print_warning(f"Minimum age is not a positive integer: {min}")
                        return self.model.prompt_and_check()
                    
                    if int(value) < 16 | int(value) > 119:
                        print_warning(f"Minimum age cannot be less than 16 or greater than 119: {min}")
                        return self.model.prompt_and_check()
                    flags["min"] = value
                case "max":
                    if not value.isdigit():
                        print_warning(f"Minimum age is not a positive integer: {max}")
                        return self.model.prompt_and_check()
                    
                    if int(value) < 17 | int(value) > 120:
                        print_warning(f"Minimum age cannot be less than 17 or greater than 120: {max}")
                        return self.model.prompt_and_check()
                    flags['max'] = value
                case _:
                    print_warning(f"Invalid argument: {split_space[0]}")
                    return self.model.prompt_and_check()
                
        flags_required = [flags['name'], flags['geo'], flags['pid']]
        true_count = sum(bool(value) for value in flags_required)

        if true_count > 2:
            print_warning("Too many parameters used")
            return self.model.prompt_and_check()
        if not true_count:
            print_warning("No parameters given")
            return self.model.prompt_and_check()
        if not flags['geo']:
            if true_count == 2:
                print_warning("Used two purple parameters")
                return self.model.prompt_and_check()

        self.model.command = "search", flags
        return True
    
    def listener(self, value, old, new):
        match value:
            case "VALIDATE":
                if self.valid_command(): self.model.fire_property_change(Change.EXECUTE)
            case _:
                return