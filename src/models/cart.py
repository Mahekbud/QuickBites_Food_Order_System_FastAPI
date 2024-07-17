from sqlalchemy import Column,String,DateTime,Boolean,ForeignKey,Integer
from datetime import datetime
import uuid
from database.database import Base



class CartItem(Base):
    __tablename__ = 'CartInfo'
    
    id = Column(String(100),primary_key=True,default=str(uuid.uuid4()))
    cart_id = Column(String(100), ForeignKey('Carts.id'), nullable=False)
    product_id = Column(String(100), ForeignKey('ProductInfo.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Integer, nullable=False)
    create_at = Column(DateTime,default=datetime.now())
    modified_at = Column(DateTime,default=datetime.now(),onupdate=datetime.now())
    is_active = Column(Boolean,default=True)
    is_deleted = Column(Boolean,default = False)
    
    
class Cart(Base):
    __tablename__ = 'Carts'

    id = Column(String(100),primary_key=True,default=str(uuid.uuid4()))
    user_id = Column(String(100), ForeignKey('UserInfo.id'), nullable=False)
    create_at = Column(DateTime, default=datetime.now())
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    