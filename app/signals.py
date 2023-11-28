import signal
import sys

from app.output.style import Style

def sigint(sig, frame):
  print(f'\n\n{Style.BOLD}{Style.WHITE}Bye!{Style.END}\n')
  sys.exit(0)

def setup():
  signal.signal(signal.SIGINT, sigint)