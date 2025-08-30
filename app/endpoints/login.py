from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from app.auth import auth_user, create_token, get_user_from_token
from app.schemas.user import User
from app.database import get_user

router = APIRouter()

@router.post("/login")
async def login_user(user: Annotated[User, Depends(auth_user)]) -> dict:
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    return {
        "access_token": create_token({"sub": user.username}),
        "token_type": "bearer"
    }

@router.get("/protected_resource")
async def about_me(username: Annotated[str, Depends(get_user_from_token)]):
    user = get_user(username)
    if user:
        return {"message": "access granted"}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")