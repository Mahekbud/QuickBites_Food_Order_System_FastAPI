from  fastapi import HTTPException,APIRouter
from database.database import Sessionlocal
from passlib.context import CryptContext
from src.schemas.category import CategoryAll,Categorypatch
from src.models.category import Category
import uuid
from logs.log_config import logger




pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Categories = APIRouter(tags=["Category"])

db = Sessionlocal()


#----------------------------create category--------------------------------

@Categories.post("/create_category", response_model=CategoryAll)
def create_category(cate: CategoryAll):
    new_category = Category(
        id=str(uuid.uuid4()),
        name=cate.name,
        description=cate.description
    )
    
    db.add(new_category)
    db.commit()
    
    logger.info(f"Created new category: {new_category.id}")
    return new_category


#----------------------------get category by id-------------------------------

@Categories.get("/get_category_by_id", response_model=CategoryAll)
def get_category_by_id(category_id: str):
    db_category = db.query(Category).filter(Category.id == category_id, Category.is_active == True, Category.is_deleted == False).first()
    
    if db_category is None:
        logger.error(f"Category not found: Category ID {category_id}")
        raise HTTPException(status_code=404, detail="Category not found")
    
    logger.info(f"Retrieved category: Category ID {category_id}")
    return db_category


#------------------------get all category------------------------------

@Categories.get("/get_all_category", response_model=list[CategoryAll])
def get_all_category():
    db_category = db.query(Category).filter(Category.is_active == True, Category.is_deleted == False).all()
    
    if not db_category:
        logger.error("No categories found")
        raise HTTPException(status_code=404, detail="Category not found")
    
    logger.info(f"Retrieved all categories, count: {len(db_category)}")
    return db_category


#--------------------------update category by put----------------------------

@Categories.put("/update_category_by_put", response_model=CategoryAll)
def update_category_by_put(category_id: str, category: CategoryAll):
    db_category = db.query(Category).filter(Category.id == category_id, Category.is_active == True, Category.is_deleted == False).first()
    
    if db_category is None:
        logger.error(f"Category not found: Category ID {category_id}")
        raise HTTPException(status_code=404, detail="Category not found")
    
    db_category.name = category.name
    db_category.description = category.description
    
    db.commit()
    logger.info(f"Updated category: Category ID {category_id}")
    return db_category


#---------------------------update category by patch------------------------------

@Categories.patch("/update_category_by_patch", response_model=Categorypatch)
def update_category_by_patch(category_id: str, category: Categorypatch):
    db_category = db.query(Category).filter(Category.id == category_id, Category.is_active == True, Category.is_deleted == False).first()
    
    if db_category is None:
        logger.error(f"Category not found: Category ID {category_id}")
        raise HTTPException(status_code=404, detail="Category not found")
    
    for key, value in category.dict(exclude_unset=True).items():
        setattr(db_category, key, value)
    
    db.commit()
    logger.info(f"Partially updated category: Category ID {category_id}, Updated fields: {', '.join(key for key in category.dict(exclude_unset=True))}")
    return db_category



#-------------------------------delete category----------------------------

@Categories.delete("/delete_category_by_id")
def delete_category_by_id(category_id: str):
    db_category = db.query(Category).filter(Category.id == category_id, Category.is_active == True, Category.is_deleted == False).first()
    
    if db_category is None:
        logger.error(f"Category not found: Category ID {category_id}")
        raise HTTPException(status_code=404, detail="Category not found")
    
    db_category.is_active = False
    db_category.is_deleted = True
    db.commit()
    
    logger.info(f"Deleted category: Category ID {category_id}")
    return {"message": "Category deleted successfully"}

    