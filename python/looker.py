from colorama import Fore, Style
from model.validator import Validator
from model.model import Model
from controller.command import Command
from view.console import Console
from view.logger import Logger
import sys
        
def repl(model: Model):
    try:
        Logger.logo()
        Logger.support((f"For help type {Fore.YELLOW}help{Style.RESET_ALL} in the command prompt\n"))

        model.prompt_and_check()
    except KeyboardInterrupt:
        print("\n")
        Logger.warning(f"Exiting the program")
        sys.exit(0)

def main():
    model = Model()
    
    Console(model)
    Command(model)
    Validator(model)
    
    repl(model)

if __name__=='__main__':
    main()