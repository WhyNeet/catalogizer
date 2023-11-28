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

    (action, catalog_name) = Prompt.action('')

    match action:
      case 's':
        if catalog_name is None:
          return Printer.warn('Catalog name is not provided.')

        (catalog, msg) = self.storage.open(catalog_name)

        if catalog is None:
          Printer.warn(f'Catalog {Style.BLUE}{catalog_name}{Style.WHITE} is broken. Erase it and create new? (Y/N)')
          if not Prompt.choice():
            return
          
          self.storage.delete(catalog_name)
          (catalog, _) = self.storage.open(catalog_name)
          Printer.info(f'Recreated catalog {Style.BLUE}{catalog_name}{Style.WHITE}.')
        
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

          catalogs[catalog_data.name] = catalog_data.topics.keys()
        
        Printer.table(catalogs)
      case 'd':
        if catalog_name is None:
          return Printer.warn('Catalog name is not provided.')

        Printer.info(self.storage.delete(catalog_name))

  def run(self):
    while True:
      self.prompt_action()