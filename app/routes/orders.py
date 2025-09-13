from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import Order, CartItem, Product
from app.schemas import OrderCreate, OrderRead
from datetime import datetime

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderRead)
def place_order(order_data: OrderCreate, session: Session = Depends(get_session)):
    cart_items = session.exec(select(CartItem)).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = 0
    for item in cart_items:
        product = session.get(Product, item.product_id)
        if not product or product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Product {item.product_id} unavailable or out of stock")
        total += product.price * item.quantity
        product.stock -= item.quantity
        session.add(product)

    order = Order(
        user_id=order_data.user_id,
        total_price=total,
        status="pending",
        created_at=datetime.utcnow()
    )
    session.add(order)
    session.commit()
    session.refresh(order)

    # Clear cart
    for item in cart_items:
        session.delete(item)
    session.commit()

    return order

@router.get("/", response_model=list[OrderRead])
def list_orders(session: Session = Depends(get_session)):
    orders = session.exec(select(Order)).all()
    return orders
