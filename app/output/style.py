class Style:
  PURPLE = '\033[95m'
  CYAN = '\033[96m'
  DARKCYAN = '\033[36m'
  BLUE = '\033[94m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  RED = '\033[91m'
  WHITE = '\033[37m'

  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'
  END = '\033[0m'

  def rgb(s: str, r: int, g: int, b: int) -> str:
    return "\x1b[38;2;{};{};{}m{}\x1b[0m".format(r, g, b, s)