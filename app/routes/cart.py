from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import CartItem, Product
from app.schemas import CartItemCreate, CartItemRead

router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/", response_model=CartItemRead)
def add_to_cart(item: CartItemCreate, session: Session = Depends(get_session)):
    product = session.get(Product, item.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    cart_item = CartItem(**item.dict())
    session.add(cart_item)
    session.commit()
    session.refresh(cart_item)
    return cart_item

@router.get("/", response_model=list[CartItemRead])
def get_cart(session: Session = Depends(get_session)):
    cart_items = session.exec(select(CartItem)).all()
    return cart_items

@router.delete("/{item_id}")
def remove_from_cart(item_id: int, session: Session = Depends(get_session)):
    item = session.get(CartItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    session.delete(item)
    session.commit()
    return {"detail": "Item removed from cart"}
