from  fastapi import HTTPException,APIRouter
from database.database import Sessionlocal
from passlib.context import CryptContext
from src.schemas.cart import CartAll,CartOptinal,Carts
from src.models.cart import Cart,CartItem
from src.models.product import Product
from datetime import datetime
import uuid
from logs.log_config import logger




pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

carts = APIRouter(tags=["Cart"])

db = Sessionlocal()



#-------------------------create cart--------------------------

@carts.post("/create_cart/")
def create_cart(user_id: str):
    db_cart = Cart(user_id=user_id)
    db.add(db_cart)
    db.commit()
    
    logger.info(f"Created new cart: {db_cart.id} for user: {user_id}")
    return {"message": "Cart created successfully"}


#---------------------add item to cart-------------------------

@carts.post("/create_cart/")
def create_cart(user_id: str):
    db_cart = Cart(user_id=user_id)
    db.add(db_cart)
    db.commit()
    
    logger.info(f"Created new cart: {db_cart.id} for user: {user_id}")
    return {"message": "Cart created successfully"}

#----------------------------get cartitem  by id----------------------------

@carts.get("/get_cartitem_by_id", response_model=CartAll)
def get_cartitem_by_id(cartitem_id: str):
    db_cart = db.query(CartItem).filter(CartItem.id == cartitem_id, CartItem.is_active == True, CartItem.is_deleted == False).first()
    
    if db_cart is None:
        logger.error(f"Cart item not found: Cart Item ID {cartitem_id}")
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    logger.info(f"Retrieved cart item: Cart Item ID {cartitem_id}")
    return db_cart


#-------------------------get all cartitem-------------------------------

@carts.get("/get_all_cartitem", response_model=list[CartAll])
def get_all_cart():
    db_cart = db.query(CartItem).filter(CartItem.is_active == True, CartItem.is_deleted == False).all()
    
    if not db_cart:
        logger.error("No cart items found")
        raise HTTPException(status_code=404, detail="Cart items not found")
    
    logger.info(f"Retrieved all cart items, count: {len(db_cart)}")
    return db_cart


#-------------------------update cartitem by put-------------------------

@carts.put("/update_cartitem_by_put", response_model=CartAll)
def update_cartitem_by_put(cartitem_id: str, cart: CartAll):
    db_cart = db.query(CartItem).filter(CartItem.id == cartitem_id, CartItem.is_active == True, CartItem.is_deleted == False).first()
    
    if db_cart is None:
        logger.error(f"Cart item not found: Cart Item ID {cartitem_id}")
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    db_product = db.query(Product).filter(Product.id == cart.product_id).first()
    if not db_product:
        logger.error(f"Product not found: Product ID {cart.product_id}")
        raise HTTPException(status_code=404, detail="Product not found")

    total_price = cart.quantity * db_product.price
    
    db_cart.cart_id = cart.cart_id
    db_cart.product_id = cart.product_id
    db_cart.quantity = cart.quantity
    db_cart.total_price = total_price
    
    db.commit()
    logger.info(f"Updated cart item: Cart Item ID {cartitem_id}")
    return db_cart

#------------------------update cart by patch---------------------------

@carts.patch("/update_cartitem_by_patch", response_model=CartOptinal)
def update_cartitem_by_patch(cartitem_id: str, cart: CartOptinal):
    db_cart = db.query(CartItem).filter(CartItem.id == cartitem_id, CartItem.is_active == True, CartItem.is_deleted == False).first()
    
    if db_cart is None:
        logger.error(f"Cart item not found: Cart Item ID {cartitem_id}")
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    db_product = db.query(Product).filter(Product.id == db_cart.product_id).first()
    if not db_product:
        logger.error(f"Product not found: Product ID {db_cart.product_id}")
        raise HTTPException(status_code=404, detail="Product not found")

    total_price = db_cart.quantity * db_product.price

    for key, value in cart.dict(exclude_unset=True).items():
        setattr(db_cart, key, value)
        
    db_cart.total_price = total_price
    
    db.commit()
    logger.info(f"Partially updated cart item: Cart Item ID {cartitem_id}")
    return db_cart



#-----------------------delete_cart_by_id------------------------

@carts.delete("/delete_cartitem_by_id")
def delete_cartitem_by_id(cartitem_id: str):
    db_cart = db.query(CartItem).filter(CartItem.id == cartitem_id, CartItem.is_active == True, CartItem.is_deleted == False).first()
    
    if db_cart is None:
        logger.error(f"Cart item not found: Cart Item ID {cartitem_id}")
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    db_cart.is_active = False
    db_cart.is_deleted = True
    db.commit()
    
    logger.info(f"Deleted cart item: Cart Item ID {cartitem_id}")
    return {"message": "Cart item deleted successfully"}



#-----------------------get cart by id-------------------------

@carts.get("/get_cart_by_id", response_model=Carts)
def get_cart_by_id(cart_id: str):
    db_cart = db.query(Cart).filter(Cart.id == cart_id, Cart.is_active == True, Cart.is_deleted == False).first()
    
    if db_cart is None:
        logger.error(f"Cart not found: Cart ID {cart_id}")
        raise HTTPException(status_code=404, detail="Cart not found")
    
    logger.info(f"Retrieved cart: Cart ID {cart_id}")
    return db_cart


#------------------------search cart id by cartitem-----------------------------

@carts.get("/get_cart_by_cartitem", response_model=list[CartAll])
def get_cart_by_cartitem(cart_id: str):
    db_cart = db.query(CartItem).filter(CartItem.cart_id == cart_id, CartItem.is_active == True, CartItem.is_deleted == False).all()
    
    if not db_cart:
        logger.error(f"Cart items not found for Cart ID: {cart_id}")
        raise HTTPException(status_code=404, detail="Cart items not found")
    
    logger.info(f"Retrieved cart items for Cart ID: {cart_id}, count: {len(db_cart)}")
    return db_cart


#--------------------------------calculate_total_price----------------------------------

@carts.get("/calculate_total_price")
def calculate_total_price(cart_id: str):
    db_cart_items = db.query(CartItem).filter(CartItem.cart_id == cart_id, CartItem.is_active == True, CartItem.is_deleted == False).all()
    
    if not db_cart_items:
        logger.error(f"No items found in the cart: Cart ID {cart_id}")
        raise HTTPException(status_code=404, detail="No items found in the cart")
    
    total_price = sum(item.total_price for item in db_cart_items)
    
    logger.info(f"Calculated total price for Cart ID {cart_id}: {total_price}")
    return {"cart_id": cart_id, "total_price": total_price}


