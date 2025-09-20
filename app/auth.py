from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, status

from app.config import load_token_config

TOKEN_CONFIG = load_token_config()


def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + \
        timedelta(minutes=TOKEN_CONFIG.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire,
        "type": "access"
    })

    return jwt.encode(
        payload=to_encode,
        key=TOKEN_CONFIG.SECRET_KEY,
        algorithm=TOKEN_CONFIG.ALGORITHM
    )


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + \
        timedelta(minutes=TOKEN_CONFIG.REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire,
        "type": "refresh"
    })

    return jwt.encode(
        payload=to_encode,
        key=TOKEN_CONFIG.SECRET_KEY,
        algorithm=TOKEN_CONFIG.ALGORITHM
    )


def get_payload_from_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token, TOKEN_CONFIG.SECRET_KEY, algorithms=[TOKEN_CONFIG.ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def validate_token_type(token: str, token_type: str) -> str | None:
    try:
        payload = jwt.decode(
            token, TOKEN_CONFIG.SECRET_KEY, algorithms=[TOKEN_CONFIG.ALGORITHM]
        )

        if payload["type"] == token_type:
            return token
        else:
            return None

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token validation error: {str(e)}",
        )