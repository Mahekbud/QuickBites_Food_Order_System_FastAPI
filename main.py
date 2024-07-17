from fastapi import FastAPI
from src.routers.user import Users
from src.routers.product import Products
from src.routers.hotel import Hotels
from src.routers.order import Orders
from src.routers.feedback import Feedbacks
from src.routers.category import Categories
from src.routers.cart import carts
from src.routers.payment import Payments
from src.routers.delivery_boy import DeliveryBoys


app = FastAPI(title="Food_order_system")


app.include_router(Users)
app.include_router(Products)
app.include_router(Hotels)
app.include_router(Orders)
app.include_router(Feedbacks)
app.include_router(Categories)
app.include_router(carts)
app.include_router(Payments)
app.include_router(DeliveryBoys)