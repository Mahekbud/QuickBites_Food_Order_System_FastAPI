from sqlalchemy import Column,String,DateTime,Boolean,ForeignKey,Integer
from datetime import datetime
import uuid
from database.database import Base



class Payment(Base):
    __tablename__ = 'PaymentInfo'
    
    id = Column(String(100),primary_key=True,default=str(uuid.uuid4()))
    user_id = Column(String(100), ForeignKey('UserInfo.id'),nullable=False)
    order_id = Column(String(100), ForeignKey('OrderInfo.id'),nullable=False)
    total_amount = Column(Integer,nullable=False)
    status = Column(String(100),default="pending")
    Payment_method = Column(String(100),nullable=False,default="Cash")
    address = Column(String(1000),nullable=False)
    create_at = Column(DateTime,default=datetime.now())
    modified_at = Column(DateTime,default=datetime.now(),onupdate=datetime.now())
    is_active = Column(Boolean,default=True)
    is_deleted = Column(Boolean,default = False)