from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime
from database.database import Base


class DeliveryBoy(Base):
    __tablename__ = 'DeliveryBoyInfo'
    
    id = Column(String(100), primary_key=True, default=str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)
    is_available = Column(Boolean, default=True)
    create_at = Column(DateTime,default=datetime.now())
    modified_at = Column(DateTime,default=datetime.now(),onupdate=datetime.now())
    is_active = Column(Boolean,default=True)
    is_deleted = Column(Boolean,default = False)