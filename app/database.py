from app.schemas.user import User
from app.security import hash_password

fake_db: list[User] = [User(username="Oleg",password=hash_password("123"))]

def get_user(user: User) -> User|None:
    username = user.username
    for user_in_db in fake_db:
        if user_in_db.username == username:
            return user_in_db
    return None

def add_user(user: User) -> User:
    hashed_password = hash_password(user.password)
    new_user = User(**user.dict(), password=hashed_password)
    fake_db.append(new_user)
    return new_user
    