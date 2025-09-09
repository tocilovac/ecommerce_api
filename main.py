from fastapi import FastAPI
from app.database import init_db
from app.routes import users

app = FastAPI(title="E-Commerce API")

# Initialize database tables
init_db()

# Include routers
app.include_router(users.router)
