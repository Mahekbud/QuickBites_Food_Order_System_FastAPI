from  fastapi import HTTPException,APIRouter
from database.database import Sessionlocal
from passlib.context import CryptContext
from src.schemas.product import ProductAll,Productpatch
from src.models.product import Product
from src.models.category import Category
import uuid
from src.models.hotel import Hotel
from sqlalchemy import func
from sqlalchemy.types import Numeric





pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Products = APIRouter(tags=["Products"])

db = Sessionlocal()


#------------------------create product-------------------------

# @Products.post("/create_product",response_model=ProductAll)
# def create_product(product:ProductAll):
    
#     new_product= Product(
#         id = str(uuid.uuid4()),
#         product_name = product.product_name,
#         price = product.price,
#         quantity = product.quantity,
#         user_id = product.user_id,
#         hotel_id = product.hotel_id,
#         category_id = product.category_id
        
#     )
   
#     db.add(new_product)
#     db.commit()
    
#     return new_product

#---------------------create_product_discount----------------------


@Products.post("/create_product", response_model=ProductAll)
def create_product(product: ProductAll):
    if not product.category_id:
        raise HTTPException(status_code=400, detail="Category ID must be provided")
 
    category = db.query(Category).filter(Category.id == product.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    discount = 0.0
    if category.name.lower() == "south indian":
        discount = 0.05  # 5% discount
    elif category.name.lower() == "italian":
        discount = 0.25  # Buy 2, get 50% off one 
    elif category.name.lower() == "chinese":
        discount = 0.10  # 10% discount
    
    discounted_price = product.price * (1 - discount)
     
    
    new_product = Product(
        id=str(uuid.uuid4()),
        product_name=product.product_name,
        price=product.price,
        discount_price=discounted_price,
        quantity=product.quantity,
        user_id=product.user_id,
        hotel_id=product.hotel_id,
        category_id=product.category_id
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return new_product
#-------------------------get product by id----------------------------------

@Products.get("/get_product_by_id",response_model=ProductAll)
def get_product_by_id(product_id : str):
    db_product = db.query(Product).filter(Product.id == product_id,Product.is_active == True,Product.is_deleted == False).first()
    
    if db_product is None:
        raise  HTTPException(status_code=404,detail="product not found")
    
    return db_product

#--------------------------get all product-------------------------

@Products.get("/get_all_product",response_model=list[ProductAll])
def get_all_product():
    db_product = db.query(Product).filter(Product.is_active == True,Product.is_deleted == False).all()
    
    if db_product is None:
        raise  HTTPException(status_code=404,detail="product not found")
    
    return db_product

#-------------------------update product by put --------------------------

@Products.put("/update_product_by_put",response_model=ProductAll)
def update_product_by_put(product_id : str,product : ProductAll):
    db_product = db.query(Product).filter(Product.id == product_id,Product.is_active == True,Product.is_deleted == False).first()
    
    if db_product is None:
        raise  HTTPException(status_code=404,detail="product not found")
    
    if not product.category_id:
        raise HTTPException(status_code=400, detail="Category ID must be provided")
 
    category = db.query(Category).filter(Category.id == product.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    discount = 0.0
    if category.name.lower() == "south indian":
        discount = 0.05  # 5% discount
    elif category.name.lower() == "italian":
        discount = 0.25  # Buy 2, get 50% off one 
    elif category.name.lower() == "chinese":
        discount = 0.10  # 10% discount
    
    discounted_price = product.price * (1 - discount)
    
    db_product.product_name = product.product_name
    db_product.price = product.price
    db_product.discount_price = discounted_price
    db_product.quantity = product.quantity
    db_product.user_id = product.user_id
    db_product.hotel_id = product.hotel_id
    db_product.category_id = product.category_id
    
    db.commit()
    return db_product

#------------------------update product by patch-------------------------

@Products.patch("/update_product_by_patch",response_model=Productpatch)
def update_product_by_patch(product_id : str,product : Productpatch):
    db_product = db.query(Product).filter(Product.id == product_id,Product.is_active == True,Product.is_deleted == False).first()
    
    if db_product is None:
        raise HTTPException(status_code=404,detail="product not found")
    
    db_product = db.query(Product).filter(Product.id == product_id,Product.is_active == True,Product.is_deleted == False).first()
    
    if db_product is None:
        raise  HTTPException(status_code=404,detail="product not found")
    
    if not product.category_id:
        raise HTTPException(status_code=400, detail="Category ID must be provided")
 
    category = db.query(Category).filter(Category.id == product.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    discount = 0.0
    if category.name.lower() == "south indian":
        discount = 0.05  # 5% discount
    elif category.name.lower() == "italian":
        discount = 0.25  # Buy 2, get 50% off one 
    elif category.name.lower() == "chinese":
        discount = 0.10  # 10% discount
    
    for key,value in product.dict(exclude_unset=True).items():
        setattr(db_product,key,value)
        
    if 'price' in product.dict(exclude_unset=True):
        db_product.discount_price = db_product.price * (1 - discount)
    
    db.commit()
    return db_product

#------------------------delete product by id--------------------------

@Products.delete("/delete_product_by_id")
def delete_product_by_id(product_id : str):
    db_product = db.query(Product).filter(Product.id == product_id,Product.is_active == True,Product.is_deleted == False).first()
    
    if db_product is None:
        raise HTTPException(status_code=404,detail="product not found")
    
    db_product.is_active=False
    db_product.is_deleted =True
    
    db.commit()
    return {"message": "product deleted successfully"}


#---------------------------search_product_by_product_name----------------------------

@Products.get("/search_product_by_product_name")
def search_product_by_product_name(product: str, min_price: float, max_price: float):
    min_price = float(min_price)
    max_price = float(max_price)

    products = db.query(Product).filter(
        Product.product_name == product,
        Product.is_active == True,
        Product.is_deleted == False,
        func.cast(Product.price, Numeric) >= min_price,
        func.cast(Product.price, Numeric) <= max_price
    ).all()
    
    result = []
    for p in products:
        hotel = db.query(Hotel).filter(Hotel.id == p.hotel_id).first()
        if hotel:
            result.append({
                "hotel_name": hotel.name,
                "product_name": p.product_name,
                "product_price": p.price
            })

    if not result:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"FoodItem": result}

