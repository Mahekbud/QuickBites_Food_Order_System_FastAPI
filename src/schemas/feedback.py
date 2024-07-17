from pydantic import BaseModel
from typing import Optional



class FeedbackAll(BaseModel):
    user_id : str
    product_id : str
    suggestion : str
    star : str
    issue : str
    
    
class Feedbackpatch(BaseModel):
     user_id : Optional[str] = None
     product_id : Optional[str] = None
     suggestion : Optional[str] = None
     star : Optional[str] = None
     issue : Optional[str] = None