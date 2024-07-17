from sqlalchemy import Column,String,DateTime,Boolean
from datetime import datetime
import uuid
from database.database import Base



class User(Base):
    __tablename__ = 'UserInfo'
    
    
    id = Column(String(100),primary_key=True,default=str(uuid.uuid4()))
    u_name = Column(String(20),nullable = False)
    email = Column(String(50),nullable = False)
    phone_no = Column(String(15),nullable = False)
    password = Column(String(100),nullable = False)
    create_at = Column(DateTime,default=datetime.now())
    modified_at = Column(DateTime,default=datetime.now(),onupdate=datetime.now())
    is_active = Column(Boolean,default=True)
    is_deleted = Column(Boolean,default = False)
    is_verified = Column(Boolean,default = False)