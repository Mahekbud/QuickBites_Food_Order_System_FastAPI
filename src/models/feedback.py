from sqlalchemy import Column,String,DateTime,Boolean,ForeignKey
from datetime import datetime
import uuid
from database.database import Base



class Feedback(Base):
    __tablename__ = 'FeedbackInfo'
    
    id = Column(String(100),primary_key=True,default=str(uuid.uuid4()))
    user_id = Column(String(100), ForeignKey('UserInfo.id'), nullable=False)
    product_id = Column(String(100),ForeignKey('ProductInfo.id'),nullable=False)
    suggestion = Column(String(500),nullable=False)
    star = Column(String(10),nullable=False)
    issue = Column(String(500),nullable=False)
    create_at = Column(DateTime,default=datetime.now())
    modified_at = Column(DateTime,default=datetime.now(),onupdate=datetime.now())
    is_active = Column(Boolean,default=True)
    is_deleted = Column(Boolean,default = False)