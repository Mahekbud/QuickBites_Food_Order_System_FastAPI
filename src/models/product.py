from sqlalchemy import Column,String,ForeignKey,DateTime,Boolean,Integer
from datetime import datetime
import uuid
from database.database import Base


class Product(Base):
    __tablename__ = 'ProductInfo'
    
    id = Column(String(100),primary_key=True,default=str(uuid.uuid4()))
    product_name = Column(String(500),nullable=False)
    price = Column(Integer,nullable=False)
    discount_price = Column(Integer, nullable=True)
    quantity = Column(Integer,nullable=False)
    user_id = Column(String(100), ForeignKey('UserInfo.id'), nullable=True)
    hotel_id = Column(String(100), ForeignKey('HotelInfo.id'), nullable=False)
    category_id = Column(String(100), ForeignKey('CategoryInfo.id'), nullable=False)
    create_at = Column(DateTime,default=datetime.now())
    modified_at = Column(DateTime,default=datetime.now(),onupdate=datetime.now())
    is_active = Column(Boolean,default=True)
    is_deleted = Column(Boolean,default = False)
    