from pydantic import BaseModel
from typing import Optional



class CategoryAll(BaseModel):
    name : str
    description : str
  
  
class Categorypatch(BaseModel):
    name : Optional[str] = None
    description  : Optional[str] = None