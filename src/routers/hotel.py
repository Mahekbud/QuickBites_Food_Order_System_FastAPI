from  fastapi import HTTPException,APIRouter
from database.database import Sessionlocal
from passlib.context import CryptContext
from src.schemas.hotel import HotelAll,HotelPatch
from src.models.hotel import Hotel
import uuid
from logs.log_config import logger





pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Hotels = APIRouter(tags=["Hotel"])

db = Sessionlocal()

@Hotels.post("/create_hotels", response_model=HotelAll)
def create_hotels(hotel: HotelAll):
    new_hotel = Hotel(
        id=str(uuid.uuid4()),
        name=hotel.name,
        address=hotel.address
    )
   
    db.add(new_hotel)
    db.commit()
    
    logger.info(f"Hotel created: Hotel ID {new_hotel.id}, Name {new_hotel.name}")
    return new_hotel

#-------------------------------get hotel by id -------------------------------

@Hotels.get("/get_hotel_by_id", response_model=HotelAll)
def get_hotel_by_id(hotel_id: str):
    db_hotel = db.query(Hotel).filter(Hotel.id == hotel_id, Hotel.is_active == True, Hotel.is_deleted == False).first()
    
    if db_hotel is None:
        logger.error(f"Hotel not found: Hotel ID {hotel_id}")
        raise HTTPException(status_code=404, detail="Hotel not found")
    
    logger.info(f"Hotel retrieved: Hotel ID {hotel_id}, Name {db_hotel.name}")
    return db_hotel

#---------------------------get all hotel----------------------------

@Hotels.get("/get_all_hotel", response_model=list[HotelAll])
def get_all_hotel():
    db_hotel = db.query(Hotel).filter(Hotel.is_active == True, Hotel.is_deleted == False).all()
    
    if not db_hotel:
        logger.error("No hotels found")
        raise HTTPException(status_code=404, detail="No hotels found")
    
    logger.info(f"All active hotels retrieved: {len(db_hotel)} hotels")
    return db_hotel

#---------------------------update hotel by put---------------------------

@Hotels.put("/update_hotel_by_put", response_model=HotelAll)
def update_hotel_by_put(hotel: HotelAll, hotel_id: str):
    db_hotel = db.query(Hotel).filter(Hotel.id == hotel_id, Hotel.is_active == True, Hotel.is_deleted == False).first()
    
    if db_hotel is None:
        logger.error(f"Hotel not found: Hotel ID {hotel_id}")
        raise HTTPException(status_code=404, detail="Hotel not found")
    
    db_hotel.name = hotel.name
    db_hotel.address = hotel.address
    
    db.commit()
    logger.info(f"Hotel updated: Hotel ID {hotel_id}, Name {db_hotel.name}")
    return db_hotel

#---------------------------update hotel by patch------------------------

@Hotels.patch("/update_hotel_by_patch", response_model=HotelPatch)
def update_hotel_by_patch(hotel: HotelPatch, hotel_id: str):
    db_hotel = db.query(Hotel).filter(Hotel.id == hotel_id, Hotel.is_active == True, Hotel.is_deleted == False).first()
    
    if db_hotel is None:
        logger.error(f"Hotel not found: Hotel ID {hotel_id}")
        raise HTTPException(status_code=404, detail="Hotel not found")
    
    for key, value in hotel.dict(exclude_unset=True).items():
        setattr(db_hotel, key, value)
    
    db.commit()
    logger.info(f"Hotel partially updated: Hotel ID {hotel_id}, Updated fields: {', '.join(key for key in hotel.dict(exclude_unset=True))}")
    return db_hotel

#----------------------------delete hotel by id-------------------------------

@Hotels.delete("/delete_hotel_by_id")
def delete_hotel_by_id(hotel_id: str):
    db_hotel = db.query(Hotel).filter(Hotel.id == hotel_id, Hotel.is_active == True, Hotel.is_deleted == False).first()
    
    if db_hotel is None:
        logger.error(f"Hotel not found: Hotel ID {hotel_id}")
        raise HTTPException(status_code=404, detail="Hotel not found")
    
    db_hotel.is_active = False
    db_hotel.is_deleted = True
    
    db.commit()
    logger.info(f"Hotel deleted: Hotel ID {hotel_id}")
    
    return {"message": "Hotel deleted successfully"}