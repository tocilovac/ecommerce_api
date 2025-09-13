from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session
from app.models import User
from app.schemas import UserCreate, UserLogin, UserRead
from app.auth import hash_password, verify_password, create_access_token
from app.crud import get_user_by_email


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserRead)
def register(user: UserCreate, session: Session = Depends(get_session)):
    try:
        existing_user = session.exec(select(User).where(User.email == user.email)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_pw = hash_password(user.password)
        print("Hashed password:", hashed_pw)

        new_user = User(
            username=user.username,
            email=user.email,
            password_hash=hashed_pw
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        print("New user created:", new_user)

        return UserRead(**new_user.dict(exclude={"password_hash"}))

    except Exception as e:
        print("Registration error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/login")
def login(credentials: UserLogin, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == credentials.email)).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token, "token_type": "bearer"}
