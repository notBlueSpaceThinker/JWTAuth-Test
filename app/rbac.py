# from fastapi import HTTPException, status
# from functools import wraps

# class PermissionChecker:
#     """Декоратор для проверки ролей пользователя"""
#     def __init__(self, roles: list[str]):
#         self.roles = roles

#     def __call__(self, func, *args, **kwds):
#         @wraps(func)
#         async def wrapper(*args, **kwargs):
#             oay= kwargs.get("payload")
#             if not user:
#                 raise HTTPException(
#                     status_code=status.HTTP_403_FORBIDDEN,
#                     detail="Autentification required"
#                 )

#             if "admin" in user.roles:
#                 return await func(*args, **kwargs)

#             if not any(role in user.toles for role in self.roles):
#                 raise HTTPException(
#                     status_code=status.HTTP_403_FORBIDDEN,
#                     detail="Insufficient access rights"
#                 )
#             return await func(*args, **kwargs)
#         return wrapper
