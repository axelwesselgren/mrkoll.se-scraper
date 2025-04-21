from typing import Dict, List
from colorama import Fore, Style
from model.model import Model
from .colors import Colors
from config.column_widths import ColumnWidths

def help_msg(msg, color):
    return f"{color}{msg}{Style.RESET_ALL}"

def get_total_width(widths: Dict[str, int]) -> int:
    return (
        ColumnWidths.ID_WIDTH + widths['name'] + ColumnWidths.AGE_WIDTH +
        widths['address'] + ColumnWidths.ZIP_WIDTH + widths['city'] +
        ColumnWidths.BIRTHDAY_WIDTH + ColumnWidths.RESIDENCY_WIDTH + ColumnWidths.GENDER_WIDTH + 25
    )

def render_header(widths: Dict[str, int]) -> str:
    header = (
        f"{'ID'.ljust(ColumnWidths.ID_WIDTH)} | "
        f"{'Full name'.ljust(widths['name'])} | "
        f"{'Age'.ljust(ColumnWidths.AGE_WIDTH)} | "
        f"{'Gender'.ljust(ColumnWidths.GENDER_WIDTH)} | "
        f"{'Birthday'.ljust(ColumnWidths.BIRTHDAY_WIDTH)} | "
        f"{'Address'.ljust(widths['address'])} | "
        f"{'ZIP'.ljust(ColumnWidths.ZIP_WIDTH)} | "
        f"{'City'.ljust(widths['city'])} | "
        f"{'Residency'.ljust(ColumnWidths.RESIDENCY_WIDTH)}"
    )
    
    return header

def render_seperator(widths: Dict[str, int]) -> str:
    return f"{Colors.SUPPORT}{'-' * get_total_width(widths)}{Colors.RESET}"

def calculate_widths(users: List[any]) -> Dict[str, int]:
    return {
        "name": max(len(user.name) for user in users),
        "address": max(len(user.address) for user in users),
        "city": max(len(user.city) for user in users),
    }
    
def render_row(user: any, index: int, widths: Dict[str, int]) -> str:
    return (
        f"{Colors.INFO}{str(index).ljust(ColumnWidths.ID_WIDTH)}{Colors.RESET} | "
        f"{user.name.ljust(widths['name'])} | "
        f"{user.age.ljust(ColumnWidths.AGE_WIDTH)} | "
        f"{user.gender.ljust(ColumnWidths.GENDER_WIDTH)} | "
        f"{user.birthday.ljust(ColumnWidths.BIRTHDAY_WIDTH)} | "
        f"{user.address.ljust(widths['address'])} | "
        f"{user.zip.ljust(ColumnWidths.ZIP_WIDTH)} | "
        f"{user.city.ljust(widths['city'])} | "
        f"{user.lived_here.ljust(ColumnWidths.RESIDENCY_WIDTH)}"
    )
    
class Console:
    def __init__(self, model: Model):
        self.model = model
        self.model.add_property_change_listener(self.listener)

    def help(self):
        save_color = Fore.GREEN if self.model.save else Fore.RED
        debug_color = Fore.GREEN if self.model.debug else Fore.RED
        
        help_lines = [
            f"{help_msg('[save]', save_color)}       - Save all information gathered to a database",
            f"{help_msg('[debug]', debug_color)}      - Print debugging information about processes",
            "",
            f"{help_msg('[--geo]', Colors.INFO)}          {help_msg('City/Street', Colors.INFO)}",
            f"{help_msg('[--gender]', Colors.INFO)}       {help_msg('Gender', Colors.INFO)}             Options {help_msg('m/w/a', Colors.HIGHLIGHT)}{help_msg('DEFAULT a', Colors.INFO)}",
            f"{help_msg('[--min]', Colors.INFO)}          {help_msg('Minimum Age', Colors.INFO)}        Type {help_msg('int', Colors.HIGHLIGHT)}       {help_msg('DEFAULT 16', Colors.INFO)}",
            f"{help_msg('[--max]', Colors.INFO)}          {help_msg('Maximum Age', Colors.INFO)}        Type {help_msg('int', Colors.HIGHLIGHT)}       {help_msg('DEFAULT 120', Colors.INFO)}",
            "",
            f"{help_msg('[search]', Colors.SUPPORT)}     - Search up people in the database using Name or PID with Optional flags",
            f"{help_msg('[next]', Colors.SUPPORT)}       - Displays another page of 20 people",
            f"{help_msg('[show]', Colors.SUPPORT)}       - Shows all people currently in search",
            f"{help_msg('[lookup]', Colors.SUPPORT)}     - Looks up the selected person using Phone, PID or Index"
        ]
        
        print("\n".join(help_lines))
        
    def show(self):
        users = self.model.results_preview
        widths = calculate_widths(users)

        print(render_header(widths))
        print(render_seperator(widths))

        for i, user in enumerate(users):
            print(render_row(user, i, widths))
    
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