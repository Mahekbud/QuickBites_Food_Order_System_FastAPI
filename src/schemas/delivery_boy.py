from pydantic import BaseModel
from typing import Optional




class DeliveryBoyAll(BaseModel):
    name : str
    phone_number : str
    email : str
    is_available : bool
  
class DeliveryBoyPatch(BaseModel):
    name : Optional[str] = None
    phone_number : Optional[str] = None
    email : Optional[str] = None
    is_available : Optional[bool]  = None
