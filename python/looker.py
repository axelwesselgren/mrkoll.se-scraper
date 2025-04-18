from colorama import Fore, Style
from view.console import print_title, print_support, print_warning, Console
from model.validator import Validator
from model.model import Model
from controller.command import Command
import sys
        
def repl(model: Model, validator: Validator, command: Command):
    try:
        print_title()

        print_support(f"For help type {Fore.YELLOW}help{Style.RESET_ALL} in the command prompt\n")

        model.prompt_and_check()
    except KeyboardInterrupt:
        print("\n")
        print_warning(f"Exiting the program")
        sys.exit(0)

def main():
    model = Model()
    console = Console(model)
    command = Command(model)
    validator = Validator(model)
    repl(model, validator, command)

if __name__=='__main__':
    main()