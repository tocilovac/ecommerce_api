from fastapi import FastAPI
from app.database import init_db
from app.routes import users, cart, orders
from app.routes.products import router as products_router
from app.routes.admin import router as admin_router

app = FastAPI(title="E-Commerce API")

init_db()

app.include_router(users.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(products_router, prefix="/products", tags=["products"])
app.include_router(admin_router)
