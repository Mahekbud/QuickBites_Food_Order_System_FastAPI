from  fastapi import HTTPException,APIRouter
from database.database import Sessionlocal
from passlib.context import CryptContext
from src.schemas.order import OrderAll,Orderpatch
from src.models.order import Order
from src.models.product import Product
from src.models.user import User
from src.models.cart import Cart,CartItem
from src.schemas.delivery import DeliveryAll
from src.models.delivery import Delivery
import uuid
from datetime import datetime
from src.utils.order_confirmation_email import send_order_confirmation_email




pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Orders = APIRouter(tags=["Orders"])

db = Sessionlocal()


#---------------------------create orders--------------------------------

@Orders.post("/create_order", response_model=OrderAll)
def create_order(order: OrderAll,delivery : DeliveryAll):
    
    product = db.query(Product).filter(Product.id == order.product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.user_id != order.user_id:
        raise HTTPException(status_code=403, detail="User did not purchase this product")

    cart = db.query(Cart).filter(Cart.id == order.cart_id).first()
    
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    if cart.user_id != order.user_id:
        raise HTTPException(status_code=403, detail="Cart does not belong to this user")

    cart_items = db.query(CartItem).filter(CartItem.cart_id == order.cart_id, CartItem.is_active == True, CartItem.is_deleted == False).all()

    if not cart_items:
        raise HTTPException(status_code=404, detail="CartItem not found")

    total_amount = sum(item.total_price for item in cart_items)

    new_order = Order(
        id=str(uuid.uuid4()),
        customer_name=order.customer_name,
        total_amount=total_amount,
        delivery_address=order.delivery_address,
        phone_number=order.phone_number,
        status="pending",
        user_id=order.user_id,
        product_id=order.product_id,
        cart_id= order.cart_id
    )

    db.add(new_order)
    db.commit()
 
    user = db.query(User).filter(User.id == order.user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_delivery = Delivery(
        id=str(uuid.uuid4()),
        order_id=new_order.id,
        delivery_boy_id=delivery.delivery_boy_id,
        delivery_status="pending"
    )
    
    db.add(new_delivery)
    new_delivery.delivery_status = "Done"
    db.commit()     

    send_order_confirmation_email(user.email, new_order)
    
    new_order.status = "done"
    db.commit()
    
    return new_order


#-------------------------get order by id----------------------------


@Orders.get("/get_order_by_id",response_model=OrderAll)
def get_order_by_id(order_id : str):
    db_order = db.query(Order).filter(Order.id == order_id,Order.is_active == True,Order.is_deleted == False).first()
    
    if db_order is None:
        raise  HTTPException(status_code=404,detail="order not found")
    
    return db_order

#-------------------------get all order--------------------

@Orders.get("/get_all_order",response_model=list[OrderAll])
def get_all_order():
    db_order = db.query(Order).filter(Order.is_active == True,Order.is_deleted == False).all()
    
    if db_order is None:
        raise  HTTPException(status_code=404,detail="order not found")
    
    return db_order

#-------------------------update order by put---------------------------

@Orders.put("/update_order_by_put",response_model=OrderAll)
def update_order_by_put(order_id : str,order : OrderAll):
    db_order = db.query(Order).filter(Order.id == order_id,Order.is_active == True,Order.is_deleted == False).first()
    
    if db_order is None:
        raise  HTTPException(status_code=404,detail="order not found")
    
    product = db.query(Product).filter(Product.id == order.product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.user_id != order.user_id:
        raise HTTPException(status_code=403, detail="User did not purchase this product")
    
    cart = db.query(Cart).filter(Cart.id == order.cart_id).first()
    
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    if cart.user_id != order.user_id:
        raise HTTPException(status_code=403, detail="Cart does not belong to this user")

    cart_items = db.query(CartItem).filter(CartItem.cart_id == order.cart_id, CartItem.is_active == True, CartItem.is_deleted == False).all()

    if not cart_items:
        raise HTTPException(status_code=404, detail="CartItem not found")

    total_amount = sum(item.total_price for item in cart_items)


    
    db_order.customer_name = order.customer_name
    db_order.total_amount = total_amount
    db_order.delivery_address = order.delivery_address
    db_order.phone_number = order.phone_number
    db_order.status = order.status
    db_order.user_id = order.user_id
    db_order.product_id = order.product_id
    db_order.cart_id = order.cart_id

  
    
    db.commit()
    return db_order

#----------------------------update order by patch----------------------------

@Orders.patch("/update_order_by_patch", response_model=Orderpatch)
def update_order_by_patch(order_id: str, order: Orderpatch):

    db_order = db.query(Order).filter(Order.id == order_id, Order.is_active == True, Order.is_deleted == False).first()

    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    product = db.query(Product).filter(Product.id == db_order.product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
 
    if order.cart_id:
        cart = db.query(Cart).filter(Cart.id == order.cart_id).first()

        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")

        if cart.user_id != db_order.user_id:
            raise HTTPException(status_code=403, detail="Cart does not belong to this user")
        
    for key, value in order.dict(exclude_unset=True).items():
        setattr(db_order, key, value)

    if order.product_id:
        db_order.product_id = order.product_id

    if db_order.product_id:
        new_product = db.query(Product).filter(Product.id == db_order.product_id).first()

        if new_product:
            db_order.total_amount = new_product.price * new_product.quantity
        else:
            db_order.total_amount = 0.0  
    db.commit()
    
    return db_order

#--------------------------delete order by id---------------------------

@Orders.delete("/delete_order_by_id")
def delete_order_by_id(order_id : str):
    db_order = db.query(Order).filter(Order.id == order_id,Order.is_active == True,Order.is_deleted == False).first()
    
    if db_order is None:
        raise  HTTPException(status_code=404,detail="order not found")
    
    db_order.is_active=False
    db_order.is_deleted =True
    
    db.commit()
    
    return {"message": "order deleted successfully"}

#-------------------------search order by product id-------------------------

@Orders.get("/search_order_by_product_id")
def search_order_by_product_id(product_id : str):
    
    db_order = db.query(Order).filter(Order.product_id == product_id,Order.is_active == True,Order.is_deleted == False).all()
    
    if db_order is None:
        raise  HTTPException(status_code=404,detail="order not found")
    
    return db_order

#---------------------------search order by user id----------------------

@Orders.get("/search_order_by_user_id")
def search_order_by_user_id(user_id : str):
    
    db_order = db.query(Order).filter(Order.user_id == user_id,Order.is_active == True,Order.is_deleted == False).all()
    
    if db_order is None:
        raise  HTTPException(status_code=404,detail="order not found")
    
    return db_order

#----------------------------cancel_order---------------------------------

@Orders.put("/cancel_order",response_model=OrderAll)
def cancel_order(order_id : str):
    
    db_order = db.query(Order).filter(Order.id == order_id,Order.is_active == True,Order.is_deleted == False).first()

    if db_order is None:
        raise  HTTPException(status_code=404,detail="order not found")
    
    db_order.status = "cancelled"
    db_order.modified_at = datetime.now()
    
    db.commit()
    return db_order

#----------------------------order get by datetime------------------------

@Orders.get("/orders_by_startdate_enddate", response_model=list[OrderAll])
def get_orders_by_date(start_date: datetime, end_date: datetime ):

    db_order = db.query(Order).filter(Order.create_at >= start_date, Order.create_at <= end_date,Order.is_active == True,Order.is_deleted == False).all()
    
    if not db_order:
        raise HTTPException(status_code=404, detail="No orders found in the specified date range")
    
    return db_order

#--------------------------------order by date-------------------------------

@Orders.get("/orders_by_date", response_model=list[OrderAll])
def get_orders_by_date(start_date: datetime ):

    db_order = db.query(Order).filter(Order.create_at >= start_date,Order.is_active == True,Order.is_deleted == False).all()
    
    if not db_order:
        raise HTTPException(status_code=404, detail="No orders found in the specified date range")
    
    return db_order
