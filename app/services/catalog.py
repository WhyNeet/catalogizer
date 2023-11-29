from app.model.catalog import Catalog
from app.input.prompt import Prompt
from app.output.printer import Printer
from app.output.style import Style
from app.services.storage import StorageService
from constants import catalog_menu_guide, topic_menu_guide

class CatalogService:
  catalog: Catalog | None = None
  topic: str | None = None
  storage: StorageService = None
  
  def __init__(self, storage: StorageService):
    self.storage = storage
  
  def prompt_action(self) -> str:
    if not self.topic is None:
      return self.prompt_topic_action()
    
    Printer.guide(catalog_menu_guide)

    (action, argument) = Prompt.action(self.catalog.name)

    match action:
      case 'c':
        if argument is None:
          return Printer.warn("Topic name is not provided.")

        Printer.info(self.catalog.add_topic(argument))
      case 's':
        if argument is None:
          return Printer.warn("Topic name is not provided.")
        
        if not argument in self.catalog.topics:
          Printer.warn(f'Topic "{argument}" does not exist.')
          return
        self.topic = argument
      case 'l':
        if self.catalog.topics:
          return Printer.list(self.catalog.topics)

        Printer.info("No topics found.")
      case 'v':
        if len(self.catalog.topics) == 0:
          return Printer.info("No topics found.")

        return Printer.table(self.catalog.topics)
      case 'f':
        if argument is None:
          return Printer.info("Search query is not provided.")

        if len(self.catalog.topics) == 0:
          return Printer.info("No topics found.")

        topics = {}

        for topic in self.catalog.topics:
          values = []
          for value in self.catalog.topics[topic]:
            idx = value.lower().find(argument)

            if idx > -1:
              values.append(value)
          
          if len(values) > 0:
            topics[topic] = values
        
        if not topics:
          return Printer.info('No values found.')
        
        return Printer.table(topics)
      case 'd':
        if argument is None:
          return Printer.warn("Topic name is not provided.")

        Printer.info(self.catalog.remove_topic(argument))
      case 'b':
        self.catalog = None
        return
      case other:
        return Printer.warn(f'Unknown command: "{other}"')
    
    self.storage.store(self.catalog)
  
  
  def prompt_topic_action(self):
    Printer.guide(topic_menu_guide)

    (action, value) = Prompt.action(f'{self.catalog.name}:{self.topic}')

    match action:
      case 'c':
        if value is None:
          return Printer.warn("Value is not provided.")
        
        Printer.info(self.catalog.append_value(self.topic, value))
      case 'd':
        if value is None:
          return Printer.warn("Value is not provided.")
        
        return Printer.info(self.catalog.remove_value(self.topic, value))
      case 'l':
        if len(self.catalog.topics[self.topic]) == 0:
          return Printer.info("No topic values found.")
        
        return Printer.list(self.catalog.topics[self.topic])
      case 'f':
        if value is None:
          return Printer.warn('Search query is not provided.')
        query = value

        if len(self.catalog.topics[self.topic]) == 0:
          return Printer.info('No topic values found.')
        
        for value in self.catalog.topics[self.topic]:
          idx = value.lower().find(query)
          if idx > -1:
            print(f" - {Style.BOLD}{Style.WHITE}{value[:idx]}{Style.BLUE}{value[idx:(idx + len(query))]}{Style.WHITE}{value[(idx + len(query)):]}{Style.END}")
        
        print()
        return
      case 'b':
        self.topic = None
        return
      case other:
        return Printer.warn(f'Unknown command: "{other}"')
    
    self.storage.store(self.catalog)