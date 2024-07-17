from pydantic import BaseModel
from typing import Optional



class HotelAll(BaseModel):
    name : str
    address : str
   
class HotelPatch (BaseModel):
    name : Optional[str] = None
    address : Optional[str] = None