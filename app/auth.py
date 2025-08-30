from datetime import datetime, timedelta
from fastapi import HTTPException, status
import jwt

from app.config import load_token_config


TOKEN_CONFIG = load_token_config()

def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=TOKEN_CONFIG.ACCESS_TOKEN_EXPIRE_MINUTES)
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