from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import HTTPException, status, Depends
import jwt 
from app.schemas.user import User
from app.config import load_token_config
from app.database import get_user
from app.security import verify_password

TOKEN_CONFIG = load_token_config()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_token(data: dict) -> str:
    return jwt.encode(data, TOKEN_CONFIG.SECRET_KEY, algorithm=TOKEN_CONFIG.ALGORITHM)

def get_user_from_token(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    try:
        payload = jwt.decode(token, TOKEN_CONFIG.SECRET_KEY, algorithms=[TOKEN_CONFIG.ALGORITHM])
        return payload.get("sub")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"}
                            )
    
def auth_user(user: User) -> User|None:
    user_in_db = get_user(user)
    if user_in_db and verify_password(user.password, user_in_db.password):
        return user_in_db
    return None