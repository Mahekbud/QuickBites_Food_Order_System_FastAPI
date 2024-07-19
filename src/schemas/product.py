from pydantic import BaseModel
from typing import Optional



class ProductAll(BaseModel):
    
    product_name : str
    price : int
    discount_price : int
    quantity : int
    user_id : str
    hotel_id : str
    category_id : str


class Productpatch(BaseModel):
    product_name : Optional[str] = None
    price : Optional[int] = None
    quantity : Optional[int] = None
    discount_price : Optional[int] = None
    user_id : Optional[str] = None
    hotel_id : Optional[str] = None
    category_id : Optional[str] = None