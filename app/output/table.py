from os import get_terminal_size
from app.output.style import Style

type Data = dict[str, list[str] | Data]

class Table:
  data: Data | None = None

  def __init__(self, data: Data) -> None:
    self.data = data

  def col_max_len(self) -> int:
    (cols, _) = get_terminal_size()

    return (cols // len(self.data)) - 2

  def col_len(data: Data, max_len: int) -> int:
    col_len = 0

    for header in data:
        col_len = min(max_len, max(col_len, len(header) + 2))
        for value in data[header]:
            col_len = min(max_len, max(col_len, len(value) + 2))
    
    return col_len

  def cut_value(val: str, max: int) -> str:
    if len(val) > max:
      return val[:(max - 5)] + '...'
    
    return val
  
  def headers(data: Data, col_len: int) -> str:
    headers = ''

    for header in data:
      header = Table.cut_value(header, col_len)
      offset = (col_len - len(header))
      headers += f'|{" " * (offset // 2)}{Style.BLUE}{header}{" " * ((offset // 2) + (col_len - len(header)) % 2)}{Style.END}'
    
    return headers + '|'
  
  def values(self, col_len: int) -> str:
    longest_topic_len = max(self.data.values(), key = len)

    values = ''
    for row in range(max(1, len(longest_topic_len))):
      for col in self.data:
        if len(self.data[col]) > row:
          value = list(self.data[col])[row]
          value = Table.cut_value(value, col_len)
          values += f'| {Style.BOLD}{value}{" " * (col_len - len(value) - 1)}{Style.END}'
        else:
          values += f'|{" " * col_len}'
      values += '|\n'
    
    return values
    
  
  def make_separator(data: Data, col_len: int) -> int:
    return '+' + '—' * (sum([(col_len + 1) for _ in range(len(data))]) - 1) + '+'
  
  def print(self):
    col_value_max_len = self.col_max_len()

    col_len = Table.col_len(self.data, col_value_max_len)
    separator = Table.make_separator(self.data, col_len)

    print(separator)

    headers = Table.headers(self.data, col_len)
    print(headers)

    print(separator)

    values = self.values(col_len)  
    print(values, end = '')

    print(separator, end = '\n\n')