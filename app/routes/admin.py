from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.models import Product, User
from app.schemas import ProductCreate, ProductRead
from app.auth import get_current_user
from app.dependencies import require_admin
from app.models import Notification 

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/products", response_model=ProductRead)
def admin_create_product(
    product: ProductCreate,
    session: Session = Depends(get_session),
    user: User = Depends(require_admin)
):
    new_product = Product(**product.dict())
    session.add(new_product)
    session.commit()
    session.refresh(new_product)

    notification = Notification(
        message=f"New product added: {new_product.name}",
        type="product_created"
    )
    session.add(notification)
    session.commit()
    return new_product

@router.get("/notifications")
def get_notifications(session: Session = Depends(get_session), user: User = Depends(require_admin)):
    return session.query(Notification).order_by(Notification.created_at.desc()).all()

@router.post("/notifications/{id}/read")
def mark_notification_as_read(id: int, session: Session = Depends(get_session), user: User = Depends(require_admin)):
    notif = session.query(Notification).get(id)
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    notif.read = True
    session.commit()
    return {"status": "marked as read"}
