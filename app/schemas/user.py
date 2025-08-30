from pydantic import BaseModel

class BaseUser(BaseModel):
    username: str

class User(BaseUser):
    password: str
    
class UserInDB(BaseUser):
    hashed_password: str