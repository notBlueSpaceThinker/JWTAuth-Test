from fastapi import (APIRouter, Depends, HTTPException, Request, Response,
                     status)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.auth import create_token, get_payload_from_token
from app.database import add_user, auth_user, get_user
from app.dependencies import get_current_user
from app.schemas.user import User

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/login")
@limiter.limit("5/minute")
async def login_user(
    request: Request, form_data: OAuth2PasswordRequestForm = Depends()
):
    if not get_user(form_data.username):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if auth_user(form_data.username, form_data.password):
        access_token = create_token({"sub": form_data.username, "type": "access"})
        refresh_token = create_token({"sub": form_data.username, "type": "refresh"}, token_type="r")

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user"
        )


@router.post("/register", status_code=status.HTTP_201_CREATED)
@limiter.limit("1/minute")
async def register_user(
    request: Request, form_data: OAuth2PasswordRequestForm = Depends()
):
    if get_user(form_data.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )

    add_user(form_data.username, form_data.password)
    access_token = create_token({"sub": form_data.username, "type": "access"})
    refresh_token = create_token({"sub": form_data.username, "type": "refresh"}, token_type="r")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/protected_resource")
async def protected_resource(current_user: User = Depends(get_current_user)):
    return {"message": f"{current_user.username}, access granted"}


@router.post("/refresh")
@limiter.limit("5/minute")
async def refresh(request: Request):
    token = await oauth2_scheme(request)

    payload = get_payload_from_token(token)
    username = payload.get("sub")

    access_token = create_token({"sub": username, "type": "access"})
    refresh_token = create_token({"sub": username, "type": "refresh"}, token_type="r")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
