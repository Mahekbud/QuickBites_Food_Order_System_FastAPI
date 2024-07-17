from pydantic import BaseModel




class DeliveryAll(BaseModel):
    order_id : str
    delivery_boy_id : str
   
    