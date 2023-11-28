from constants import app_title
from app.app import App
from app.signals import setup

def main():
  setup()

  app = App(app_title)

  app.run()

main()