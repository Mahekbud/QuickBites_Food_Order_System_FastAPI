from pydantic import BaseModel



class PaymentAll(BaseModel):
    user_id : str
    order_id : str
    Payment_method : str
    address : str

class PaymentBase(BaseModel):
    user_id : str
    order_id : str
    total_amount : int
    status : str
    Payment_method : str
    address : str
    
class PaymentOut(BaseModel):
    payment_id :str