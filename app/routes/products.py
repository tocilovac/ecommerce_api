from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session
from app.models import Product
from app.schemas import ProductCreate, ProductRead
from app.cache import get_cached_products, set_cached_products

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=ProductRead)
def create_product(product: ProductCreate, session: Session = Depends(get_session)):
    new_product = Product(**product.dict())
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product

@router.get("/", response_model=list[ProductRead])
def list_products(session: Session = Depends(get_session)):
    products = session.exec(select(Product)).all()
    return products

@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()

@router.get("/", response_model=list[ProductRead])
def list_products(session: Session = Depends(get_session)):
    cached = get_cached_products()
    if cached:
        return cached

    products = session.exec(select(Product)).all()
    set_cached_products(products)
    return products
