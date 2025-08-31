from typing import Literal
from datetime import datetime, timedelta
from fastapi import HTTPException, status
import jwt

from app.config import load_token_config


TOKEN_CONFIG = load_token_config()

def create_token(data: dict, token_type: Literal['a', 'r'] = 'a') -> str:
    """Создание токена из словаря. 
    token_type: 'a' - access_token; 'r' - refresh_token"""

    to_encode = data.copy()

    if token_type == 'a':
        expire = datetime.utcnow() + timedelta(minutes=TOKEN_CONFIG.ACCESS_TOKEN_EXPIRE_MINUTES)
    elif token_type == 'r':
        expire = datetime.utcnow() + timedelta(minutes=TOKEN_CONFIG.REFRESH_TOKEN_EXPIRE_MINUTES)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token_type"
        )
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        TOKEN_CONFIG.SECRET_KEY,
        algorithm=TOKEN_CONFIG.ALGORITHM
    )
    return encoded_jwt

def get_payload_from_token(token: str) -> dict:
    try: 
        payload = jwt.decode(
            token, 
            TOKEN_CONFIG.SECRET_KEY, 
            algorithms=[TOKEN_CONFIG.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )