from  fastapi import HTTPException,APIRouter
from database.database import Sessionlocal
from passlib.context import CryptContext
from src.schemas.payment import PaymentAll,PaymentBase
from src.models.payment import Payment
from src.models.order import Order
from src.routers.order import Order
import uuid



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Payments = APIRouter(tags=["Payment"])

db = Sessionlocal()


#------------------------create payment---------------------------

@Payments.post("/create_payment",response_model=PaymentAll)
def create_payment(payment:PaymentAll):

    order = db.query(Order).filter(Order.id == payment.order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.user_id != payment.user_id:
        raise HTTPException(status_code=403, detail="User did not purchase this product")
    
    existing_payment = db.query(Payment).filter(Payment.order_id == payment.order_id).first()
    
    if existing_payment:
        raise HTTPException(status_code=400, detail="Payment for this order has already been completed")
     
    total_amount = order.total_amount
    
    new_payment= Payment(
        id = str(uuid.uuid4()),
        user_id = payment.user_id,
        order_id = payment.order_id,
        total_amount = total_amount,
        status = "pending",
        Payment_method = payment.Payment_method,
        address = payment.address  
    )
   
    db.add(new_payment)
    new_payment.status = "Done"
    db.commit()
    
    return new_payment


#-----------------------------get payment by id----------------------------

@Payments.get("/get_payment_by_id",response_model=PaymentAll)
def get_payment_by_id(payment_id : str):
    
    db_payment = db.query(Payment).filter(Payment.id == payment_id,Payment.is_active == True,Payment.is_deleted == False).first()
    
    if not db_payment:
        raise HTTPException(status_code=404, detail="payment not found") 
    
    return db_payment

#----------------------------get all payment------------------------------

@Payments.get("/get_all_payment",response_model=list[PaymentAll])
def get_all_payment():
    
    db_payment = db.query(Payment).filter(Payment.is_active == True,Payment.is_deleted == False).all()
    
    if not db_payment:
        raise HTTPException(status_code=404, detail="payment not found") 
    
    return db_payment

#----------------------------delete payment by id---------------------------------

@Payments.delete("/delete_payment_by_id")
def delete_payment_by_id(payment_id : str):
    
    db_payment = db.query(Payment).filter(Payment.id == payment_id,Payment.is_active == True,Payment.is_deleted == False).first()
    
    if not db_payment:
        raise HTTPException(status_code=404, detail="payment not found") 
    
    db_payment.is_active = False
    db_payment.is_deleted = True
    
    db.commit()
    return {"message":"payment delete succesfully"}

#---------------------------search user by payment-------------------------------

@Payments.get("/search_user_by_payment",response_model=list[PaymentBase])
def search_user_by_payment(user_id : str):
    
    db_payment = db.query(Payment).filter(Payment.user_id == user_id,Payment.is_active == True,Payment.is_deleted == False).all()
    
    if not db_payment:
        raise HTTPException(status_code=404, detail="payment not found") 
    
    return db_payment




