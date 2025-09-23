from fastapi import HTTPException, status
from functools import wraps

class PermissionChecker:

    def __init__(self, roles: list[str]):
        self.roles = roles

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get("current_user")
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Autentification required"
                )

            if "admin" in current_user.roles:
                return await func(*args, **kwargs)

            if not any(role in current_user.roles for role in self.roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient access rights"
                )
            return await func(*args, **kwargs)
        return wrapper
