from fastapi import FastAPI
from app.database import init_db
from app.routes import users
from app.routes import products
from app.routes import cart
from app.routes import orders

app = FastAPI(title="E-Commerce API")  # ✅ Define app first

# Initialize database tables
init_db()

# Include routers
app.include_router(users.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)
