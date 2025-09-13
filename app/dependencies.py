from fastapi import Depends, HTTPException
from app.auth import get_current_user
from app.models import User

def require_admin(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user
