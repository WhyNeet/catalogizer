from app.output.style import Style
from typing import Iterable
from app.output.table import Table

type Guide = list[list[str]]
type TableType = dict[str, list[str]]

class Printer:
  def info(message: str):
    print(Style.BOLD, Style.WHITE, f'{message}\n', Style.END)
  
  def warn(message: str):
    print(Style.BOLD, Style.RED, f'{message}\n', Style.END)
  
  def list(list: Iterable):
    for val in list:
      print(f'- {Style.BOLD}{Style.BLUE}{val}{Style.END}')
    print()
  
  def guide(guide: Guide):
    print(Printer.__stringify_guide(guide), sep = '')
  
  def __stringify_guide(guide: Guide) -> str:
    s = ''

    for action in guide:
      s += f"{Style.BOLD}{action[0]}{Style.END} - {action[1]}\n"

    return s

  def table(data: TableType):
    table = Table(data)
    table.print()