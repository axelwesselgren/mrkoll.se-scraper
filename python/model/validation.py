import re
from .regex import Regex

class Validation:
    @staticmethod
    def validate_gender(value: str):
        if value not in ["m", "w", "a"]:
            raise ValueError(f"Not a valid gneder: {value}")
        
        return value

    @staticmethod
    def validate_age(value: str, is_min: bool):
        if not value.isdigit():
            raise ValueError(f"Minimum age is not a positive integer: {value}")
        
        if is_min:
            if int(value) < 16 or int(value) > 119:
                raise ValueError(f"Minimum age cannot be less than 16 or greater than 119: {value}")
        else:
            if int(value) < 17 or int(value) > 120:
                raise ValueError(f"Minimum age cannot be less than 17 or greater than 120: {value}")

        return value
    
    @staticmethod
    def validate_phone(value: str):
        if not re.match(Regex.SWEDISH_PHONE, value):
            raise ValueError(f"Not a valid Swedish phone number: {value}")
        
        return value
    
    @staticmethod
    def validate_index(value: any, length: int):
        if not value.isdigit():
            raise ValueError("Invalid selection, not a positive integer")

        if int(value) >= length:
            raise ValueError("Selection not in list")
        
        return value
    
    @staticmethod
    def validate_pid(value: str):
        if not re.match(Regex.PID_WITH_4, value):
            raise ValueError(f"Not a valid Swedish PID: {value}")
        
        return value.replace(" ", "").replace("-", "")
    
    @staticmethod
    def validate_name(value: str):
        if not re.match(Regex.SWEDISH_NAME, value):
            raise ValueError(f"Not a valid name: {value}")
        
        return value
        
    @staticmethod
    def validate_pid(value: str):
        if not re.match(Regex.PID, value):
            raise ValueError(f"Not a valid PID: {value}")
        
        if value[0:2] == "20" or value[0:2] == "19":
            if len(value) == 6:
                raise ValueError("Not a valid PID")
        
        return value