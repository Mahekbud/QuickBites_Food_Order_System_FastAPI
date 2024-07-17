from sqlalchemy import Column,String,DateTime
from datetime import datetime
import uuid
from database.database import Base




class Otps(Base):
    __tablename__ = 'OtpsInfo'
    
    id = Column(String(100),primary_key=True,default=str(uuid.uuid4()))
    email = Column(String(100),nullable= False)
    otp = Column(String(50),nullable= False)
    expiration_time = Column(DateTime,nullable= False ,default=datetime.now)
    