from app.output.style import Style
from app.output.printer import Printer

class Prompt:
  def prompt(path: str) -> str:
    inp = input(Style.rgb(f"/{path}> ", 0, 0, 160))
    
    print()
    
    return inp

  def action(path: str) -> (str, str | None):
    action_input = Prompt.prompt(path).split(' ', 1)
    if len(action_input) == 0:
      return Printer.info('Action is not provided. Usage: <action> <argument>')

    if len(action_input) == 1:
      return (action_input[0].lower(), None)
    else:
      action_input[1] = action_input[1].strip()
      if len(action_input[1]) == 0:
        return (action_input[0].lower(), None)
      return (action_input[0].lower(), action_input[1])

  def choice(path: str) -> bool | None:
    p = Prompt.prompt(path).lower()
    
    while p != 'n' and p != 'y':
      p = Prompt.prompt(path).lower()
    
    return p == 'y'