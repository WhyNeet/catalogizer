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

    (action, topic_name) = Prompt.action(self.catalog.name)

    match action:
      case 'c':
        if topic_name is None:
          return Printer.warn("Topic name is not provided.")

        Printer.info(self.catalog.add_topic(topic_name))
      case 's':
        if topic_name is None:
          return Printer.warn("Topic name is not provided.")
        
        if not topic_name in self.catalog.topics:
          Printer.warn(f'Topic "{topic_name}" does not exist.')
          return
        self.topic = topic_name
      case 'l':
        if self.catalog.topics:
          return Printer.list(self.catalog.topics)

        Printer.info("No topics found.")
      case 'd':
        if topic_name is None:
          return Printer.warn("Topic name is not provided.")

        Printer.info(self.catalog.remove_topic(topic_name))
      case 'b':
        self.catalog = None
        return
    
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
        
        Printer.info(self.catalog.remove_value(self.topic, value))
      case 'l':
        if len(self.catalog.topics[self.topic]) > 0:
          return Printer.list(self.catalog.topics[self.topic])
        
        Printer.info("No topic values found.")
      case 'b':
        self.topic = None
        return
    
    self.storage.store(self.catalog)
      
    