from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean
from datetime import datetime
from database.database import Base
import uuid



class Delivery(Base):
    __tablename__ = 'DeliveryInfo'
    
    id = Column(String(100), primary_key=True, default=str(uuid.uuid4()))
    order_id = Column(String(100), ForeignKey('OrderInfo.id'), nullable=False)
    delivery_boy_id = Column(String(100),ForeignKey('DeliveryBoyInfo.id'),nullable=False)
    delivery_status = Column(String(100), default="pending")
    create_at = Column(DateTime, default=datetime.now())
    modified_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)