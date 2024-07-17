from sqlalchemy import Column,String,ForeignKey,DateTime,Boolean,Integer
import uuid
from datetime import datetime
from database.database import Base


class Order(Base):
    __tablename__ = 'OrderInfo'
    
    id = Column(String(100),primary_key=True,default=str(uuid.uuid4()))
    customer_name = Column(String(100), nullable=False)
    total_amount = Column(Integer, nullable=False)
    delivery_address = Column(String(1000), nullable=False)
    phone_number = Column(String(20), nullable=False)
    status = Column(String(50),default="pending")
    user_id = Column(String(100), ForeignKey('UserInfo.id'), nullable=False)
    product_id = Column(String(100), ForeignKey('ProductInfo.id'), nullable=False)
    cart_id = Column(String(100),ForeignKey('Carts.id'), nullable=False)
    create_at = Column(DateTime,default=datetime.now())
    modified_at = Column(DateTime,default=datetime.now(),onupdate=datetime.now())
    is_active = Column(Boolean,default=True)
    is_deleted = Column(Boolean,default = False)