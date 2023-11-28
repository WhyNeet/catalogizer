import json
from typing import Self

class Catalog:
  name = None
  topics: dict[str, list[str]] = {}

  def __init__(self, name: str):
    self.name = name
  
  def add_topic(self, topic: str) -> str:
    if topic in self.topics:
      return f'Topic "{topic}" already exists.'

    self.topics[topic] = []

    return f'Created topic "{topic}".'
  
  def remove_topic(self, topic: str) -> str:
    if not topic in self.topics:
      return f'Topic "{topic}" does not exist.'
    
    del self.topics[topic]

    return f'Deleted topic "{topic}".'
  
  def append_value(self, topic: str, value: str) -> str:
    if not topic in self.topics:
      return f'Topic "{topic}" does not exist.'
    
    self.topics[topic].append(value)

    return f'Added value "{value}" to topic "{topic}".'
  
  def remove_value(self, topic: str, value: str) -> str:
    if not topic in self.topics:
      return f'Topic "{topic}" does not exist.'
    if not value in self.topics[topic]:
      return f'No value "{value}" found in topic "{topic}"'
    
    self.topics[topic].remove(value)

    return f'Removed value "{value}" from topic "{topic}"'
  

  def serialize(self) -> str:
    return json.dumps({ "topics": self.topics })
  
  def __str__(self) -> str:
    return self.serialize()
  
  def deserialize(s: str, name: str) -> Self | None:
    data = json.loads(s)
    
    if not "topics" in data:
      return None

    catalog = Catalog(name)
    catalog.topics = data["topics"]

    return catalog