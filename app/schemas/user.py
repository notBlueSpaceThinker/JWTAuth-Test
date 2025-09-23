from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    username: str
    full_name: str | None = None
    email: EmailStr | None = None
    disabled: bool | None = None
    roles: list[str]


class User(BaseUser):
    password: str


class UserInDB(BaseUser):
    hashed_password: str
