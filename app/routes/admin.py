from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.models import Product, User
from app.schemas import ProductCreate, ProductRead
from app.auth import get_current_user
from app.dependencies import require_admin

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/products", response_model=ProductRead)
def admin_create_product(product: ProductCreate, session: Session = Depends(get_session), user: User = Depends(require_admin)):
    new_product = Product(**product.dict())
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product
