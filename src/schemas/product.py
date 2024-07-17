from pydantic import BaseModel
from typing import Optional



class ProductAll(BaseModel):
    
    product_name : str
    price : int
    quantity : int
    user_id : str
    hotel_id : str
    category_id : str


class Productpatch(BaseModel):
    product_name : Optional[str] = None
    price : Optional[str] = None
    quantity : Optional[str] = None
    user_id : Optional[str] = None
    hotel_id : Optional[str] = None
    category_id : Optional[str] = None