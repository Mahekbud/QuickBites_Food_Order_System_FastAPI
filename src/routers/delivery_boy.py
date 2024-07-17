from  fastapi import HTTPException,APIRouter
from database.database import Sessionlocal
from passlib.context import CryptContext
from src.schemas.delivery_boy import DeliveryBoyAll,DeliveryBoyPatch
from src.models.delivery_boy import DeliveryBoy
import uuid



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DeliveryBoys = APIRouter(tags=["DeliveryBoy"])

db = Sessionlocal()

#------------------------create_delivery_boy-------------------------------

@DeliveryBoys.post("/create_delivery_boy", response_model=DeliveryBoyAll)
def create_delivery_boy(delivery_boy: DeliveryBoyAll):

    new_delivery_boy = DeliveryBoy(
        id=str(uuid.uuid4()),
        name=delivery_boy.name,
        phone_number=delivery_boy.phone_number,
        email=delivery_boy.email,
        is_available=delivery_boy.is_available
    )
    
    db.add(new_delivery_boy)
    db.commit()
    
    return new_delivery_boy

#---------------------------get_delivery_boy_by_id---------------------------

@DeliveryBoys.get("/get_delivery_boy_by_id", response_model=DeliveryBoyAll)
def get_delivery_boy_by_id(deliveryboy_id : str):
    
    db_deliveryboy = db.query(DeliveryBoy).filter(DeliveryBoy.id == deliveryboy_id,DeliveryBoy.is_active == True,DeliveryBoy.is_deleted == False).first()
    
    if db_deliveryboy is None:
        raise  HTTPException(status_code=404,detail="deliveryboy not found")
    
    return db_deliveryboy

#------------------------get_all_delivery_boy-----------------------

@DeliveryBoys.get("/get_all_delivery_boy", response_model=list[DeliveryBoyAll])
def get_all_delivery_boy():
    
    db_deliveryboy = db.query(DeliveryBoy).filter(DeliveryBoy.is_active == True,DeliveryBoy.is_deleted == False).all()
    
    if db_deliveryboy is None:
        raise  HTTPException(status_code=404,detail="deliveryboy not found")
    
    return db_deliveryboy

#---------------------------update_deliveryboy_by_put-------------------------

@DeliveryBoys.put("/update_deliveryboy_by_put", response_model=DeliveryBoyAll)
def update_deliveryboy_by_put(deliveryboy_id : str,deliveryboy : DeliveryBoyAll):
    
    db_deliveryboy = db.query(DeliveryBoy).filter(DeliveryBoy.id == deliveryboy_id,DeliveryBoy.is_active == True,DeliveryBoy.is_deleted == False).first()
    
    if db_deliveryboy is None:
        raise  HTTPException(status_code=404,detail="deliveryboy not found")
    
    db_deliveryboy.name = deliveryboy.name
    db_deliveryboy.phone_number = deliveryboy.phone_number
    db_deliveryboy.email = deliveryboy.email
    db_deliveryboy.is_available = deliveryboy.is_available
    
    db.commit()
    return db_deliveryboy

#-----------------------------update_deliveryboy_by_patch-----------------------------------


@DeliveryBoys.patch("/update_deliveryboy_by_patch", response_model=DeliveryBoyPatch)
def update_deliveryboy_by_patch(deliveryboy_id : str,deliveryboy : DeliveryBoyPatch):
    
    db_deliveryboy = db.query(DeliveryBoy).filter(DeliveryBoy.id == deliveryboy_id,DeliveryBoy.is_active == True,DeliveryBoy.is_deleted == False).first()
    
    if db_deliveryboy is None:
        raise  HTTPException(status_code=404,detail="deliveryboy not found")
     
    for key, value in deliveryboy.dict(exclude_unset=True).items():
        setattr(db_deliveryboy, key, value)
        
    db.commit()
    return db_deliveryboy

#-----------------------------delete_delivery_boy_by_id-------------------------------------

@DeliveryBoys.delete("/delete_delivery_boy_by_id")
def delete_delivery_boy_by_id(deliveryboy_id : str):
    
    db_deliveryboy = db.query(DeliveryBoy).filter(DeliveryBoy.id == deliveryboy_id,DeliveryBoy.is_active == True,DeliveryBoy.is_deleted == False).first()
    
    if db_deliveryboy is None:
        raise  HTTPException(status_code=404,detail="deliveryboy not found")
    
    db_deliveryboy.is_active = False
    db_deliveryboy.is_deleted = True
    
    db.commit()
    return {"message" : "delivery deleted successfully"}
