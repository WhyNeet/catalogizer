import signal
import sys

def sigint(sig, frame):
  print('\nBye!\n')
  sys.exit(0)

def setup():
  signal.signal(signal.SIGINT, sigint)