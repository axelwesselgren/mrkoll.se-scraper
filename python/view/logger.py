from .colors import Colors
from .labels import LOGO, Labels
import random

class Logger:
  @staticmethod
  def format_message(color: str, label: str, msg: str) -> str:
      print(f"{color}{label} {Colors.RESET}{msg}")
  
  @staticmethod
  def support(msg: str) -> None:
      Logger.format_message(Colors.SUPPORT, Labels.SUPPORT, msg)
  
  @staticmethod
  def warning(msg: str) -> None:
      Logger.format_message(Colors.WARNING, Labels.WARNING, msg)
  
  @staticmethod
  def info(msg: str) -> None:
      Logger.format_message(Colors.INFO, Labels.INFO, msg)
  
  @staticmethod
  def success(msg: str) -> None:
      Logger.format_message(Colors.SUCCESS, Labels.SUCCESS, msg)
  
  @staticmethod
  def logo() -> None:
      chosen_color = Colors.TITLE_OPTIONS[random.randint(0, len(Colors.TITLE_OPTIONS) - 1)]
      print(f"{chosen_color}{LOGO}{Colors.RESET}")