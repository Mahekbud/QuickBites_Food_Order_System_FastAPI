from  fastapi import HTTPException,APIRouter
from database.database import Sessionlocal
from passlib.context import CryptContext
from src.schemas.cart import CartAll,CartOptinal,Carts
from src.models.cart import Cart,CartItem
from src.models.product import Product
from datetime import datetime
import uuid



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

carts = APIRouter(tags=["Cart"])

db = Sessionlocal()



#-------------------------create cart--------------------------

@carts.post("/create_cart/")
def create_cart( user_id: str):
    db_cart = Cart(user_id=user_id)
    db.add(db_cart)
    db.commit()
    return {"message": "Cart created successfully"}

#---------------------add item to cart-------------------------

@carts.post("/add_item_to_cart", response_model=CartAll)
def add_item_to_cart(cart_id: str, item: CartAll):
    db_cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not db_cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    db_product = db.query(Product).filter(Product.id == item.product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    total_price = item.quantity * db_product.price
    
   

    db_cart_item = CartItem(
        id = str(uuid.uuid4()),
        cart_id=cart_id,
        product_id=item.product_id,
        quantity=item.quantity,
        total_price=total_price
    )

    db.add(db_cart_item)
    db.commit()

    db_cart.modified_at = datetime.now()
    db.commit()

    return db_cart_item

#----------------------------get cartitem  by id----------------------------

@carts.get("/get_cartitem_by_id",response_model=CartAll)
def get_cartitem_by_id(cartitem_id : str):
    db_cart = db.query(CartItem).filter(CartItem.id == cartitem_id,CartItem.is_active == True,CartItem.is_deleted == False).first()
    
    if db_cart is None:
        raise  HTTPException(status_code=404,detail="cartitem not found")
    
    return db_cart

#-------------------------get all cartitem-------------------------------

@carts.get("/get_all_cartitem",response_model=list[CartAll])
def get_all_cart():
    db_cart = db.query(CartItem).filter(CartItem.is_active == True,CartItem.is_deleted == False).all()
    
    if db_cart is None:
        raise  HTTPException(status_code=404,detail="cartitem not found")
    
    return db_cart

#-------------------------update cartitem by put-------------------------

@carts.put("/update_cartitem_by_put",response_model=CartAll)
def update_cartitem_by_put(cartitem_id : str,cart : CartAll):
    db_cart = db.query(CartItem).filter(CartItem.id == cartitem_id,CartItem.is_active == True,CartItem.is_deleted == False).first()
    
    if db_cart is None:
        raise  HTTPException(status_code=404,detail="cartitem not found")
    
    db_product = db.query(Product).filter(Product.id == cart.product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    total_price = cart.quantity * db_product.price
    
    db_cart.cart_id = cart.cart_id
    db_cart.product_id = cart.product_id
    db_cart.quantity = cart.quantity
    db_cart.total_price = total_price
    
    db.commit()
    return db_cart

#------------------------update cart by patch---------------------------

@carts.patch("/update_cartitem_by_patch",response_model=CartOptinal)
def update_cartitem_by_patch(cartitem_id : str,cart : CartOptinal):
    db_cart = db.query(CartItem).filter(CartItem.id == cartitem_id,CartItem.is_active == True,CartItem.is_deleted == False).first()
    
    if db_cart is None:
        raise  HTTPException(status_code=404,detail="cartitem not found")
    
    db_product = db.query(Product).filter(Product.id == db_cart.product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    total_price = db_cart.quantity * db_product.price

    for key,value in cart.dict(exclude_unset=True).items():
        setattr(db_cart,key,value)
        
    db_cart.total_price = total_price
        
    db.commit()
    return db_cart


#-----------------------delete_cart_by_id------------------------

@carts.delete("/delete_cartitem_by_id")
def delete_cartitem_by_id(cartitem_id : str):
    db_cart = db.query(CartItem).filter(CartItem.id == cartitem_id,CartItem.is_active == True,CartItem.is_deleted == False).first()
    
    if db_cart is None:
        raise  HTTPException(status_code=404,detail="cartitem not found")
    
    db_cart.is_active=False
    db_cart.is_deleted =True
    
    db.commit()
    
    return {"carts delete successfully"}


#-----------------------get cart by id-------------------------

@carts.get("/get_cart_by_id",response_model=Carts)
def get_cart_by_id(cart_id : str):
    db_cart = db.query(Cart).filter(Cart.id == cart_id,Cart.is_active == True,Cart.is_deleted == False).first()
    
    if db_cart is None:
        raise  HTTPException(status_code=404,detail="cart not found")
    
    return db_cart


#------------------------search cart id by cartitem-----------------------------

@carts.get("/get_cart_by_cartitem",response_model=list[CartAll])
def get_cartitem_by_id(cart_id : str):
    db_cart = db.query(CartItem).filter(CartItem.cart_id == cart_id,CartItem.is_active == True,CartItem.is_deleted == False).all()
    
    if db_cart is None:
        raise  HTTPException(status_code=404,detail="cartitem not found")
    
    return db_cart


#--------------------------------calculate_total_price----------------------------------

@carts.get("/calculate_total_price")
def calculate_total_price(cart_id: str):
    db_cart_items = db.query(CartItem).filter(CartItem.cart_id == cart_id, CartItem.is_active == True, CartItem.is_deleted == False).all()
    
    if not db_cart_items:
        raise HTTPException(status_code=404, detail="No items found in the cart")
    
    total_price = sum(item.total_price for item in db_cart_items)
    
    return {"cart_id": cart_id, "total_price": total_price}

