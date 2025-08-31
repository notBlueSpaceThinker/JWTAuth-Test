from fastapi import APIRouter, Response, Request, HTTPException, status
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.auth import create_access_token, get_payload_from_token
from app.database import auth_user, add_user, get_user
from app.schemas.user import User

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/login")
@limiter.limit("5/minute")
async def login_user(user: User, response: Response, request: Request):
    if not get_user(user.username):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if auth_user(user.username, user.password):
        token = create_access_token({"sub": user.username})

        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            samesite="lax",
            secure=False
        )

        return {"message": "Logged in successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized user"
        )
    
@router.post("/register", status_code=status.HTTP_201_CREATED)
@limiter.limit("1/minute")
async def register_user(user: User, response: Response, request: Request):
    if get_user(user.username):
        raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="User already exists"
    )
    add_user(user.username, user.password)
    token = create_access_token({"sub": user.username})

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False
    )
    return {"message": "New user created"}
    
@router.get("/protected_resource")
async def protected_resource(request: Request):
    token = request.cookies.get("access_token")
    if not token:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No access token in cookies",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    payload = get_payload_from_token(token)
    username = payload.get("sub")
    if not username:
                 raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    
    return {"message": f"{username}, access granted"}