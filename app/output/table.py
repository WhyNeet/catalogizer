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
  
  def headers(data: Data, col_len: int) -> int:
    headers = '\n'

    for header in data:
      if len(header) > col_len:
        header = header[:(col_len - 3)] + '...'
      headers += f'| {Style.BLUE}{header}{" " * (col_len - len(header) - 1)}{Style.END}'
    
    return headers + '|'
  
  def values(self, col_len: int) -> str:
    longest_topic_len = max(self.data.values(), key = len)

    values = ''
    for row in range(max(1, len(longest_topic_len))):
      for col in self.data:
        if len(self.data[col]) > row:
          value = list(self.data[col])[row]
          if len(value) > col_len:
            value = value[:(col_len - 5)] + '...'
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

    headers = Table.headers(self.data, col_len)
    print(headers)

    separator = Table.make_separator(self.data, col_len)
    print(separator)

    values = self.values(col_len)  
    print(values)