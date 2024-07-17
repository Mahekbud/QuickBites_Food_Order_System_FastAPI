from sqlalchemy import Column,String,DateTime,Boolean
from datetime import datetime
import uuid
from database.database import Base


class Category(Base):
    __tablename__ = 'CategoryInfo'
    
    id = Column(String(100),primary_key=True,default=str(uuid.uuid4()))
    name = Column(String(100),nullable=False)
    description  = Column(String(2000),nullable=False)
    create_at = Column(DateTime,default=datetime.now())
    modified_at = Column(DateTime,default=datetime.now(),onupdate=datetime.now())
    is_active = Column(Boolean,default=True)
    is_deleted = Column(Boolean,default = False)