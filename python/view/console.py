from colorama import Fore, Style
from model.model import Model
import random

colors = [Fore.MAGENTA, Fore.MAGENTA, Fore.RED, Fore.GREEN, Fore.YELLOW]

title = """
 ██▓     ▒█████   ▒█████   ██ ▄█▀▓█████  ██▀███  
▓██▒    ▒██▒  ██▒▒██▒  ██▒ ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒
▒██░    ▒██░  ██▒▒██░  ██▒▓███▄░ ▒███   ▓██ ░▄█ ▒
▒██░    ▒██   ██░▒██   ██░▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄  
░██████▒░ ████▓▒░░ ████▓▒░▒██▒ █▄░▒████▒░██▓ ▒██▒
░ ▒░▓  ░░ ▒░▒░▒░ ░ ▒░▒░▒░ ▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░
░ ░ ▒  ░  ░ ▒ ▒░   ░ ▒ ▒░ ░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░
  ░ ░   ░ ░ ░ ▒  ░ ░ ░ ▒  ░ ░░ ░    ░     ░░   ░ 
    ░  ░    ░ ░      ░ ░  ░  ░      ░  ░   ░     
"""

def print_title():
    print(colors[random.randint(0, len(colors) - 1)] + title + Style.RESET_ALL)

def get_msg(color, label, msg, printMsg=False):
    string = f"{color}{label} {Style.RESET_ALL}{msg}"
    if printMsg: print(string)
    return string

def print_support(msg):
    get_msg(Fore.MAGENTA, "[SUPPORT]", msg, True)

def print_warning(msg):
    get_msg(Fore.RED, "[WARNING]", msg, True)

def print_info(msg):
    get_msg(Fore.YELLOW, "[INFO]", msg, True)

def print_success(msg):
    get_msg(Fore.GREEN, "[SUCCESS]", msg, True)

class Console:
    def __init__(self, model: Model):
        self.model = model
        self.model.add_property_change_listener(self.listener)

    def help(self):
        save = Fore.GREEN if self.model.save else Fore.RED
        debug = Fore.GREEN if self.model.debug else Fore.RED

        print(f"{save}[save]{Style.RESET_ALL}       - Save all information gathered to a database")
        print(f"{debug}[debug]{Style.RESET_ALL}      - Print debugging information about processes")

        print(f"\n{Fore.YELLOW}[--geo]{Style.RESET_ALL}          {Fore.YELLOW}City/Street{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[--gender]{Style.RESET_ALL}       {Fore.YELLOW}Gender{Style.RESET_ALL}             Options {Style.RESET_ALL}{Fore.CYAN}m{Style.RESET_ALL}/{Fore.CYAN}w{Style.RESET_ALL}/{Fore.CYAN}a{Style.RESET_ALL}{Fore.YELLOW}  DEFAULT {Style.RESET_ALL}{Fore.CYAN}a{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[--min]{Style.RESET_ALL}          {Fore.YELLOW}Minimum Age{Style.RESET_ALL}        Type {Fore.CYAN}int{Style.RESET_ALL}       {Fore.YELLOW}DEFAULT {Style.RESET_ALL}{Fore.CYAN}16{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[--max]{Style.RESET_ALL}          {Fore.YELLOW}Maximum Age{Style.RESET_ALL}        Type {Fore.CYAN}int{Style.RESET_ALL}       {Fore.YELLOW}DEFAULT {Style.RESET_ALL}{Fore.CYAN}120{Style.RESET_ALL}")

        print(f"\n{Fore.MAGENTA}[search]{Style.RESET_ALL}     - Search up people in the database using Name or PID with Optional flags")
        print(f"{Fore.MAGENTA}[next]{Style.RESET_ALL}       - Displays another page of 20 people")
        print(f"{Fore.MAGENTA}[show]{Style.RESET_ALL}       - Shows all people currently in search")
        print(f"{Fore.MAGENTA}[lookup]{Style.RESET_ALL}     - Looks up the selected person using Phone, PID or Index")

    def show(self):
        id_width = 3
        name_width = max(len(user.name) for user in self.model.results_preview)
        age_width = 3
        address_width = max(len(user.address) for user in self.model.results_preview)
        zip_width = 5
        city_width = max(len(user.city) for user in self.model.results_preview)
        birthday_width = 10
        residency_width = 9
        gender_width = 6

        print(f"{'ID'.ljust(id_width)} | {'Full name'.ljust(name_width)} | {'Age'.ljust(age_width)} | {'Gender'.ljust(gender_width)} | {'Birthday'.ljust(birthday_width)} | {'Address'.ljust(address_width)} | {'ZIP'.ljust(zip_width)} | {'City'.ljust(city_width)} | {'Residency'.ljust(residency_width)}") 
        print(f"{Fore.MAGENTA}{'-' * (id_width + name_width + age_width + address_width + zip_width + city_width + birthday_width + residency_width + gender_width + 25)}{Style.RESET_ALL}")

        for i, user in enumerate(self.model.results_preview):
            user_id = str(i).ljust(id_width)
            full_name = user.name.ljust(name_width)
            age = user.age.ljust(age_width)
            gender = user.gender.ljust(gender_width)
            birthday = user.birthday.ljust(birthday_width)
            address = user.address.ljust(address_width)
            zip = user.zip.ljust(zip_width)
            city = user.city.ljust(city_width)
            residency = user.lived_here.ljust(residency_width)

            print(f"{Fore.YELLOW}{user_id}{Style.RESET_ALL} | {full_name} | {age} | {gender} | {birthday} | {address} | {zip} | {city} | {residency}")
    
    def listener(self, value, old, new):
        match value:
            case "HELP":
                self.help()
                return
            case "SHOW":
                self.show()
                return
            case _:
                return
