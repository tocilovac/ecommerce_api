from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel

#User Schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    created_at: datetime

#Product Schemas
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    category: Optional[str] = None
    image_url: Optional[str] = None

class ProductRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    stock: int
    category: Optional[str]
    image_url: Optional[str]
    created_at: datetime

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

class CartItemRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    added_at: datetime

class OrderCreate(BaseModel):
    user_id: int

class OrderRead(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: str
    created_at: datetime

class ProductUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category: Optional[str] = None
    image_url: Optional[str] = None


