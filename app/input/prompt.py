from app.output.style import Style
from app.output.printer import Printer

class Prompt:
  def prompt() -> str:
    inp = input(Style.rgb("/> ", 0, 0, 160))
    
    print()
    
    return inp

  def action() -> (str, str | None):
    action_input = Prompt.prompt().split(' ', 1)
    if len(action_input) == 0:
      return Printer.info('Action is not provided. Usage: <action> <argument>')
    
    if len(action_input) == 1:
      return (action_input[0].lower(), None)
    else:
      return (action_input[0].lower(), action_input[1])

  def choice() -> bool | None:
    p = Prompt.prompt().lower()
    
    while p != 'n' and p != 'y':
      p = Prompt.prompt().lower()
    
    return p == 'y'