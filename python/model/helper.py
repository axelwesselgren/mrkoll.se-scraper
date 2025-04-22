class Helper:
    @staticmethod
    def check_for_flags(command: str):
        cmd = command.split("--")[0].strip()
        dash_index = command.find("-")
        
        if dash_index == -1:
            cmd = command.split(" ")[0]
            
        return cmd

    @staticmethod
    def validate_and_update_values(validators: dict, flag_name: str, value: any, flags: dict):
        if flag_name not in validators:
            raise ValueError(f"Invalid argument: {flag_name}")
        
        validated_value = validators[flag_name](value)
        flags[flag_name] = validated_value
        
        return flags
    
    @staticmethod
    def check_and_update_flags(self, command: str, validators: dict, flags: dict):
        flag_and_values = command.split("--")
        for i in range(1, len(flag_and_values), 1):
            pair = flag_and_values[i].split(" ")
            
            flag_name = pair[0]
            flag_value = " ".join(pair[1:]).strip()

            if (len(flag_value) <= 1):
                raise ValueError(f"No value given to the flag: {flag_name}")
            
            self.validate_and_update_values(validators, flag_name, flag_value, flags)
            
    @staticmethod
    def check_and_update_arguments(self, command: str, validators: dict, flags: dict):
        value = " ".join(command.split(" ")[1:])
        
        for validator in validators:
            self.validate_and_update_values(validators, validator, value, flags)