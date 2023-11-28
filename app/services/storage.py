import os

from app.model.catalog import Catalog

class StorageService:
  location = None

  def __init__(self, location: str):
    self.location = location
    self.__init_storage()

  def __init_storage(self):
    if not os.path.exists(self.location):
      os.mkdir(self.location)
  
  def __make_catalog_path(self, name: str) -> str:
    return os.path.join(self.location, name)

  def store(self, catalog: Catalog):
    path = self.__make_catalog_path(catalog.name)

    flag = "w"

    if not os.path.exists(path):
      flag = "x"

    f = open(path, flag)

    f.write(str(catalog))

  def open(self, catalog_name: str) -> (Catalog | None, str):
    path = self.__make_catalog_path(catalog_name)

    if not os.path.exists(path):
      catalog = Catalog(catalog_name)
      self.store(catalog)
      return (catalog, f'Created catalog "{catalog_name}".')
    
    data = open(path, 'r')
    
    return (Catalog.deserialize(data.read(), catalog_name), f'Opened catalog "{catalog_name}".')
  
  def delete(self, catalog_name: str) -> str:
    path = self.__make_catalog_path(catalog_name)

    if not os.path.exists(path):
      return f'Catalog "{catalog_name}" does not exist.'
    
    os.remove(path)

    return f'Deleted catalog "{catalog_name}".'
  
  def list(self) -> list[str]:
    files = os.listdir(self.location)

    return files