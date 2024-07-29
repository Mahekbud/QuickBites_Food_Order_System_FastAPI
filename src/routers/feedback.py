from  fastapi import HTTPException,APIRouter
from database.database import Sessionlocal
from passlib.context import CryptContext
from src.schemas.feedback import FeedbackAll,Feedbackpatch
from src.models.feedback import Feedback
from src.models.product import Product
import uuid
from logs.log_config import logger




pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Feedbacks = APIRouter(tags=["Feedback"])

db = Sessionlocal()

#---------------------------create feedback---------------------------

@Feedbacks.post("/create_feedbacks", response_model=FeedbackAll)
def create_feedbacks(feedback: FeedbackAll):
    
    product = db.query(Product).filter(Product.id == feedback.product_id).first()
    
    if not product:
        logger.error(f"Product not found: Product ID {feedback.product_id}")
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.user_id != feedback.user_id:
        logger.warning(f"User did not purchase this product: User ID {feedback.user_id}, Product ID {feedback.product_id}")
        raise HTTPException(status_code=403, detail="User did not purchase this product")
    
    new_feedback = Feedback(
        id=str(uuid.uuid4()),
        user_id=feedback.user_id,
        product_id=feedback.product_id,
        suggestion=feedback.suggestion,
        star=feedback.star,
        issue=feedback.issue
    )
   
    db.add(new_feedback)
    db.commit()
    
    logger.info(f"Created new feedback: {new_feedback.id}")
    return new_feedback
#----------------------------get feedback by id-------------------------


@Feedbacks.get("/get_feedback_by_id", response_model=FeedbackAll)
def get_feedback_by_id(feedback_id: str):
    db_feedback = db.query(Feedback).filter(Feedback.id == feedback_id, Feedback.is_active == True, Feedback.is_deleted == False).first()
    
    if db_feedback is None:
        logger.error(f"Feedback not found: Feedback ID {feedback_id}")
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    logger.info(f"Retrieved feedback: Feedback ID {feedback_id}")
    return db_feedback



#------------------------get all feedback---------------------------

@Feedbacks.get("/get_all_feedback", response_model=list[FeedbackAll])
def get_all_feedback():
    db_feedback = db.query(Feedback).filter(Feedback.is_active == True, Feedback.is_deleted == False).all()
    
    if not db_feedback:
        logger.error("No feedback found")
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    logger.info(f"Retrieved all feedbacks, count: {len(db_feedback)}")
    return db_feedback


#---------------------------update feedback by put-------------------------

@Feedbacks.put("/update_feedback_by_put", response_model=FeedbackAll)
def update_feedback_by_put(feedback_id: str, feedback: FeedbackAll):
    db_feedback = db.query(Feedback).filter(Feedback.id == feedback_id, Feedback.is_active == True, Feedback.is_deleted == False).first()
    
    if db_feedback is None:
        logger.error(f"Feedback not found: Feedback ID {feedback_id}")
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    product = db.query(Product).filter(Product.id == feedback.product_id).first()
    if not product:
        logger.error(f"Product not found: Product ID {feedback.product_id}")
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.user_id != feedback.user_id:
        logger.warning(f"User did not purchase this product: User ID {feedback.user_id}, Product ID {feedback.product_id}")
        raise HTTPException(status_code=403, detail="User did not purchase this product")
    
    db_feedback.user_id = feedback.user_id
    db_feedback.product_id = feedback.product_id
    db_feedback.suggestion = feedback.suggestion
    db_feedback.star = feedback.star
    db_feedback.issue = feedback.issue
    
    db.commit()
    logger.info(f"Updated feedback: Feedback ID {feedback_id}")
    return db_feedback


#----------------------------update feedback by patch--------------------------------

@Feedbacks.patch("/update_feedback_by_patch", response_model=Feedbackpatch)
def update_feedback_by_patch(feedback_id: str, feedback: Feedbackpatch):
    db_feedback = db.query(Feedback).filter(Feedback.id == feedback_id, Feedback.is_active == True, Feedback.is_deleted == False).first()
    
    if db_feedback is None:
        logger.error(f"Feedback not found: Feedback ID {feedback_id}")
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    product = db.query(Product).filter(Product.id == db_feedback.product_id).first()
    if not product:
        logger.error(f"Product not found: Product ID {db_feedback.product_id}")
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.user_id != db_feedback.user_id:
        logger.warning(f"User did not purchase this product: User ID {db_feedback.user_id}, Product ID {db_feedback.product_id}")
        raise HTTPException(status_code=403, detail="User did not purchase this product")
    
    for key, value in feedback.dict(exclude_unset=True).items():
        setattr(db_feedback, key, value)
        
    db.commit()
    logger.info(f"Partially updated feedback: Feedback ID {feedback_id}, Updated fields: {', '.join(key for key in feedback.dict(exclude_unset=True))}")
    return db_feedback


#--------------------------delete feedback by id---------------------------

@Feedbacks.delete("/delete_feedback_by_id")
def delete_feedback_by_id(feedback_id: str):
    db_feedback = db.query(Feedback).filter(Feedback.id == feedback_id, Feedback.is_active == True, Feedback.is_deleted == False).first()
    
    if db_feedback is None:
        logger.error(f"Feedback not found: Feedback ID {feedback_id}")
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    db_feedback.is_active = False
    db_feedback.is_deleted = True
    
    db.commit()
    logger.info(f"Deleted feedback: Feedback ID {feedback_id}")
    return {"message": "Feedback deleted successfully"}


#-----------------------------avreage feedback----------------------------

@Feedbacks.get("/average_feedback")
def average_feedback():
    db_feedback = db.query(Feedback).filter(Feedback.is_active == True, Feedback.is_deleted == False).all()
    
    if not db_feedback:
        logger.error("No feedback found")
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    total_stars = sum(int(feedback.star) for feedback in db_feedback)
    average_rating = total_stars / len(db_feedback)
    
    logger.info(f"Calculated average feedback rating: {average_rating}")
    return {"average_rating": average_rating}


#---------------------------get product_id by feedback-----------------------

@Feedbacks.get("/get_product_id_by_feedback", response_model=list[FeedbackAll])
def get_product_id_by_feedback(product_id: str):
    db_feedback = db.query(Feedback).filter(Feedback.product_id == product_id, Feedback.is_active == True, Feedback.is_deleted == False).all()
    
    if not db_feedback:
        logger.error(f"No feedback found for product: Product ID {product_id}")
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    logger.info(f"Retrieved feedbacks for product: Product ID {product_id}, Count: {len(db_feedback)}")
    return db_feedback

# #----------------------------highest feedback----------------------------

# @Feedbacks.get("/highest_feedback",response_model=list[FeedbackAll])
# def highest_feedback():
#     db_feedback = db.query(Feedback).filter(Feedback.is_active == True,Feedback.is_deleted == False).all()
    
#     if db_feedback is None:
#         raise  HTTPException(status_code=404,detail="Feedback not found")
    
#     highest_feedback = max(db_feedback, key=lambda feedback: int(feedback.star))
    
#     return highest_feedback

# #------------------------lowest feedback--------------------------

# @Feedbacks.get("/lowest_feedback",response_model=list[FeedbackAll])
# def lowest_feedback():
#     db_feedback = db.query(Feedback).filter(Feedback.is_active == True,Feedback.is_deleted == False).all()
    
#     if db_feedback is None:
#         raise  HTTPException(status_code=404,detail="Feedback not found")
    
#     lowest_feedback = min(db_feedback, key=lambda feedback: int(feedback.star))
    
#     lowest_feedbacks = [
#         FeedbackAll(
#             id=feedback.id,
#             user_id=feedback.user_id,
#             product_id=feedback.product_id,
#             suggestion=feedback.suggestion,
#             star=feedback.star,
#             issue=feedback.issue
#         ) for feedback in db_feedback if int(feedback.star) == lowest_feedback
#     ]
    
#     return lowest_feedbacks
