from app.output.style import Style
from app.input.prompt import Prompt
from constants import catalog_select_guide
from app.services.storage import StorageService
from app.services.catalog import CatalogService
from app.output.printer import Printer

class App:
  storage: StorageService = StorageService("catalogize")
  catalog: CatalogService = CatalogService(storage)

  def __init__(self, app_title: str):
    print("\n ", Style.BOLD, Style.BLUE, app_title, Style.END, sep = "", end = "\n\n")
  
  def prompt_action(self):
    if not self.catalog.catalog is None:
      return self.catalog.prompt_action()

    Printer.guide(catalog_select_guide)

    (action, argument) = Prompt.action('')

    match action:
      case 's':
        if argument is None:
          return Printer.warn('Catalog name is not provided.')

        (catalog, msg) = self.storage.open(argument)

        if catalog is None:
          Printer.warn(f'Catalog {Style.BLUE}{argument}{Style.WHITE} is broken. Erase it and create new? (Y/N)')
          if not Prompt.choice():
            return
          
          self.storage.delete(argument)
          (catalog, _) = self.storage.open(argument)
          Printer.info(f'Recreated catalog {Style.BLUE}{argument}{Style.WHITE}.')
        
        Printer.info(msg)

        self.catalog.catalog = catalog
      case 'l':
        catalogs = self.storage.list()

        if len(catalogs) == 0:
          return Printer.info('No catalogs found.')

        return Printer.list(catalogs)
      case 'v':
        catalog_names = self.storage.list()
        if len(catalog_names) == 0:
          return Printer.info("No catalogs found.")

        catalogs = {}

        for catalog in catalog_names:
          (catalog_data, _) = self.storage.open(catalog)
          if catalog_data is None:
            continue

          catalogs[catalog_data.name] = catalog_data.topics
        
        if len(catalogs) == 0:
          return Printer.info("No catalogs found.")

        return Printer.table(catalogs)
      case 'f':
        if argument is None:
          return Printer.info('No search query provided.')
        
        catalog_names = self.storage.list()
        if len(catalog_names) == 0:
          return Printer.info("No catalogs found.")
        
        catalogs = {}

        for catalog in catalog_names:
          (catalog_data, _) = self.storage.open(catalog)
          for topic in catalog_data.topics:
            topic_vals = []
            for value in catalog_data.topics[topic]:
              query_idx = value.find(argument)
              if query_idx > -1:
                topic_vals.append(value)
            if len(topic_vals) != 0:
              catalogs[f'{catalog}:{topic}'] = topic_vals
        
        if len(catalogs) == 0:
          return Printer.info('No results.')
        
        print(catalogs)

        return Printer.table(catalogs)
      case 'd':
        if argument is None:
          return Printer.warn('Catalog name is not provided.')

        Printer.info(self.storage.delete(argument))

  def run(self):
    while True:
      self.prompt_action()