from pydantic import BaseModel
from typing import Optional



class UserAll(BaseModel):
    u_name : str
    email : str
    phone_no : str
    password : str
    
class UserPatch(BaseModel):
    u_name : Optional[str] = None
    email : Optional[str] = None
    phone_no : Optional[str] = None
    password : Optional[str] = None
    
class Userpass(BaseModel):
    password : str
    
    

    