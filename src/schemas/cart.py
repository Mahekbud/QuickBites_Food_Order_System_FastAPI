from pydantic import BaseModel
from typing import Optional



class CartAll(BaseModel):
    cart_id : str
    product_id : str
    quantity : int
    total_price : int

class CartOptinal(BaseModel):
    cart_id : Optional[str] = None
    product_id : Optional[str] = None
    quantity : Optional[int] = None
    total_price : Optional[int] = None
    
class Carts(BaseModel):
     user_id : str