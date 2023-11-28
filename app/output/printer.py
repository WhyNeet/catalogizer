from app.output.style import Style
from typing import Iterable
from os import get_terminal_size

type Guide = list[list[str]]
type Table = dict[str, list[str]]

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
  
  def table(dict: Table):
    (cols, _) = get_terminal_size()
    row_value_max_len = (cols // len(dict)) - 2

    col_len = 0
    headers = ''
    for header in dict:
      col_len = min(row_value_max_len, max(col_len, len(header) + 2))
      for value in dict[header]:
        col_len = min(row_value_max_len, max(col_len, len(value) + 2))
    
    for header in dict:
      if len(header) > row_value_max_len:
        header = header[:(row_value_max_len - 3)] + '...'
      headers += f'| {Style.BLUE}{header}{" " * (col_len - len(header) - 1)}{Style.END}'
    
    print(headers + '|')
    
    separator = '+' + '—' * (sum([(col_len + 1) for _ in range(len(dict))]) - 1) + '+'
    print(separator)

    longest_topic_len = max(dict.values(), key = len)

    values = ''
    for row in range(max(1, len(longest_topic_len))):
      for col in dict:
        if len(dict[col]) > row:
          value = list(dict[col])[row]
          if len(value) > row_value_max_len:
            value = value[:(row_value_max_len - 5)] + '...'
          values += f'| {Style.BOLD}{value}{" " * (col_len - len(value) - 1)}{Style.END}'
        else:
          values += f'|{" " * col_len}'
      values += '|\n'
    
    print(values)