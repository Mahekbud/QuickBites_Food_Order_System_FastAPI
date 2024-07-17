from pydantic import BaseModel




class OTPRequest(BaseModel):
    email : str
   
   
class OTPsend(BaseModel):
    email : str
    otp : str
    
class OTPALL(BaseModel):
    email : str
    otp : str
    expiration_time : str