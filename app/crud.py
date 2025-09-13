from sqlmodel import Session, select
from app.models import Product, User, Order

# Products
def get_product_by_id(session: Session, product_id: int):
    return session.get(Product, product_id)

def list_all_products(session: Session):
    return session.exec(select(Product)).all()

# Users
def get_user_by_email(session: Session, email: str):
    return session.exec(select(User).where(User.email == email)).first()

def get_user_by_id(session: Session, user_id: int):
    return session.get(User, user_id)

# Orders
def list_orders_by_user(session: Session, user_id: int):
    return session.exec(select(Order).where(Order.user_id == user_id)).all()
