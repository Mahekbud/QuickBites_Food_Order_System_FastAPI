from  fastapi import HTTPException,APIRouter
from database.database import Sessionlocal
from passlib.context import CryptContext
from src.schemas.hotel import HotelAll,HotelPatch
from src.models.hotel import Hotel
import uuid




pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Hotels = APIRouter(tags=["Hotel"])

db = Sessionlocal()

#-----------------------------create hotel---------------------------------

@Hotels.post("/create_hotels",response_model=HotelAll)
def create_hotels(hotel:HotelAll):
  
    new_hotel= Hotel(
        id = str(uuid.uuid4()),
        name = hotel.name,
        address = hotel.address
    )
   
    db.add(new_hotel)
    db.commit()
    
    return new_hotel

#-------------------------------get hotel by id -------------------------------

@Hotels.get("/get_hotel_by_id",response_model=HotelAll)
def get_hotel_by_id(hotel_id : str):
    db_hotel = db.query(Hotel).filter(Hotel.id == hotel_id,Hotel.is_active == True,Hotel.is_deleted == False).first()
    
    if db_hotel is None:
        raise  HTTPException(status_code=404,detail="hotel not found")
    
    return db_hotel

#---------------------------get all hotel----------------------------

@Hotels.get("/get_all_hotel",response_model=list[HotelAll])
def get_all_hotel():
    db_hotel = db.query(Hotel).filter(Hotel.is_active == True , Hotel.is_deleted == False).all()
    
    if db_hotel is None:
        raise HTTPException(status_code=404,detail="hotel not found")
    
    return db_hotel

#---------------------------update hotel by put---------------------------

@Hotels.put("/update_hotel_by_put",response_model=HotelAll)
def update_hotel_by_put(hotel : HotelAll,hotel_id : str):
    db_hotel = db.query(Hotel).filter(Hotel.id == hotel_id,Hotel.is_active == True,Hotel.is_deleted == False).first()
    
    if db_hotel is None:
        raise HTTPException(status_code=404,detail="hotel not found")
    
    db_hotel.name = hotel.name
    db_hotel.address = hotel.address
    
    db.commit()
    return db_hotel

#---------------------------update hotel by patch------------------------

@Hotels.patch("/update_hotel_by_patch",response_model=HotelPatch)
def update_hotel_by_patch(hotel : HotelPatch,hotel_id : str):
    db_hotel = db.query(Hotel).filter(Hotel.id == hotel_id,Hotel.is_active == True,Hotel.is_deleted == False).first()
    
    if db_hotel is None:
        raise HTTPException(status_code=404,detail="hotel not found")
    
    for key,value in hotel.dict(exclude_unset=True).items():
        setattr(db_hotel,key,value)
    
    db.commit()
    return db_hotel
    
#----------------------------delete hotel by id-------------------------------

@Hotels.delete("/delete_hotel_by_id")
def delete_hotel_by_id(hotel_id : str ):
    
    db_hotel = db.query(Hotel).filter(Hotel.id == hotel_id,Hotel.is_active == True,Hotel.is_deleted == False).first()
    
    if db_hotel is None:
        raise HTTPException(status_code=404,detail="hotel not found")
    
    db_hotel.is_active=False
    db_hotel.is_deleted =True
    
    db.commit()
    
    return {"message": "hotel deleted successfully"}