from  fastapi import HTTPException,APIRouter,Header
from database.database import Sessionlocal
from passlib.context import CryptContext
from src.schemas.user import UserAll,UserPatch,Userpass
from src.models.user import User
import uuid
import random
from src.schemas.otp import OTPsend
from src.models.otp import Otps
from datetime import timedelta,datetime
from src.utils.otp import send_otp_via_email
from src.utils.token import get_token,decode_token_user_id




pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Users = APIRouter(tags=["User"])

db = Sessionlocal()


#---------------------------create user----------------------------

@Users.post("/create_user",response_model=UserAll)
def create_user(user:UserAll):
    
    existing_user = db.query(User).filter(User.u_name == user.u_name).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="email already exists")
    

    new_user= User(
        id = str(uuid.uuid4()),
        u_name = user.u_name,
        email = user.email,
        phone_no = user.phone_no,
        password = pwd_context.hash(user.password)
    )
    
    db.add(new_user)
    db.commit()
    return new_user

#----------------------------generet otp--------------------------------

        
@Users.post("/generate_otp")
def generate_otp(user_email: str):
    otp_value = ''.join(str(random.randint(0, 9)) for _ in range(6))
    expiration_time = datetime.now() + timedelta(minutes=10)
    otp_id = str(uuid.uuid4())
    
    user_info = db.query(User).filter(User.email == user_email).first()
    if user_info is None:
        print("Invalid email")
        raise HTTPException(status_code=400, detail="Invalid email")
    
    otp_record = Otps(
        id=otp_id,
        email=user_email,
        otp=otp_value,
        expiration_time=expiration_time,
    )
    
    db.add(otp_record)
    db.commit()
    
    send_otp_via_email(user_email, otp_value)
    
    print(f"Generated OTP for {user_email}: {otp_value}")
 
    return {"message": "OTP generated successfully", "username": user_email}

#-------------------------------verify otp---------------------------

@Users.post("/verify_otp")
def verify_otp_endpoint(request: OTPsend):
    email = request.email
    entered_otp = request.otp

    stored_otp = db.query(Otps).filter(Otps.email == email).first()

    if stored_otp:
        if datetime.now() < stored_otp.expiration_time:
    
            if entered_otp == stored_otp.otp:
                db.delete(stored_otp)
                db.commit()
                
                user = db.query(User).filter(User.email == email).first()
                if user:
                    user.is_verified = True
                    db.commit()
                    return {"message": "OTP verification successful"}

                else:
                    return {"error": "User not found"}
            else:
                return {"error": "Incorrect OTP entered"}
        else:
            db.delete(stored_otp)
            db.commit()
            return {"error": "OTP has expired"}
    else:
        return {"error": "No OTP record found for the user"}
    
#--------------------------login --------------------------------

@Users.get("/login")
def login(uname : str , password : str):
    db_user = db.query(User).filter(User.u_name == uname, User.is_active == True , User.is_deleted == False).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not pwd_context.verify(password,db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
   
    access_token = get_token(db_user.id)
    return access_token

#----------------------------get by id token---------------------------------------

@Users.get("/get_user_by_token")
def get_token_id(token = Header(...)):
    user_id = decode_token_user_id(token)
    db_user = db.query(User).filter(User.id == user_id , User.is_active == True,User.is_deleted == False, User.is_verified == True ).first()
    if db_user is  None:
        raise HTTPException(status_code=404,detail="user not found")
    return db_user

#----------------------------get all-----------------------------

@Users.get("/get_all_user",response_model=list[UserAll])
def get_all_user():
    db_user = db.query(User).filter(User.is_active == True,User.is_deleted == False , User.is_verified == True).all()
    if db_user is  None:
        raise HTTPException(status_code=404,detail="user not found")
    return db_user

#-----------------------------update user by put-----------------------

@Users.put("/update_user_by_put",response_model=UserAll)
def update_user_by_put(usern: UserAll,token = Header(...)):
    user_id = decode_token_user_id(token)
    db_user = db.query(User).filter(User.id == user_id,User.is_active == True,User.is_deleted == False , User.is_verified == True).first()
    if db_user is  None:
        raise HTTPException(status_code=404,detail="user not found")
    
    existing_user = db.query(User).filter(User.u_name == usern.u_name).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    existing_email = db.query(User).filter(User.email == usern.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="email already exists")
    
    db_user.u_name = usern.u_name
    db_user.email = usern.email
    db_user.phone_no = usern.phone_no
    db_user.password = pwd_context.hash(usern.password)
    
    db.commit()
    return db_user
   
#----------------------------update user by patch----------------------------

@Users.patch("/update_user_by_token_patch",response_model=UserPatch)
def update_user_token(user : UserPatch,token = Header(...) ):
    user_id = decode_token_user_id(token)

    db_user = db.query(User).filter(User.id == user_id , User.is_active == True,User.is_deleted == False , User.is_verified == True).first()
  
    if db_user is None:
        raise HTTPException (status_code=404,detail="user not found")
    
    for key,value in user.dict(exclude_unset=True).items():
        if key == "password":
            value = pwd_context.hash(value)
        setattr(db_user,key,value)
    
    db.commit()
    return db_user

    
#------------------------------delete user---------------------------------

@Users.delete("/user_by_delete")
def delete_user_token(token = Header(...)):
    user_id = decode_token_user_id(token)
    
    db_user = db.query(User).filter(User.id == user_id,User.is_active == True, User.is_deleted == False , User.is_verified == True).first()
    
    if db_user is None:
        raise HTTPException (status_code=404,detail="user not found")
    
    db_user.is_active=False
    db_user.is_deleted =True
    
    db.commit()
    return {"message": "user deleted successfully"}


#------------------------------reregister user---------------------------

@Users.put("/reregister_user")
def rergister_users( user1: Userpass,token = Header(...) ):
    user_id = decode_token_user_id(token)
    db_user = db.query(User).filter(User.id == user_id, User.is_active == False,User.is_deleted == True , User.is_verified == True).first()
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if db_user.is_deleted is True and db_user.is_active is False:
        if pwd_context.verify(user1.password, db_user.password):
       
            db_user.is_deleted = False
            db_user.is_active = True
            db.commit()  
            return True 
 
    raise HTTPException(status_code=401, detail="Invalid credentials")


#------------------------------forgetpassword user--------------------------

@Users.put("/forget_password_token")
def forget_Password(user_newpass : str,token = Header(...)):
    user_id = decode_token_user_id (token)
    db_users = db.query(User).filter(User.id == user_id ,User.is_active == True,User.is_deleted == False , User.is_verified == True).first()
    if db_users is  None:
        raise HTTPException(status_code=404,detail="user not found")

    db_users.password = pwd_context.hash(user_newpass)
    
    db.commit()
    return "Forget Password successfully"

#---------------------------reset password--------------------------------

@Users.put("/reset_password_token")
def reset_password_token( user_oldpass: str, user_newpass: str,token = Header(...) ):
    user_id = decode_token_user_id(token)
    db_user = db.query(User).filter(User.id == user_id,User.is_active == True,User.is_deleted == False , User.is_verified == True).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if pwd_context.verify(user_oldpass , db_user.password):
        db_user.password = pwd_context.hash(user_newpass)
        db.commit()
        return "Password reset successfully"
    else:
        return "old password not matched"
    
#----------------------------current_user------------------------------------
        
@Users.get("/current_user")
def read_current_user(token: str = Header(...)):
    user_id = decode_token_user_id(token)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": user.u_name, "email": user.email}



