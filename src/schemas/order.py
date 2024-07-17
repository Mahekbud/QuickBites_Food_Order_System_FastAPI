from pydantic import BaseModel
from typing import Optional



class OrderAll(BaseModel):
    customer_name : str
    total_amount : int
    status : str
    user_id : str
    product_id : str
    cart_id : str
    delivery_address : str
    phone_number : str 
    
    
class Orderpatch(BaseModel):
    customer_name : Optional[str] = None
    total_amount : Optional[int] = None
    status : Optional[str] = None
    user_id : Optional[str] = None
    product_id : Optional[str] = None
    cart_id : Optional[str] = None
    delivery_address : Optional[str] = None
    phone_number : Optional[str] = None