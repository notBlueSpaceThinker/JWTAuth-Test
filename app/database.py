from hmac import compare_digest

from app.schemas.user import User, UserInDB
from app.security import hash_password, verify_password

fake_db: list[User] = []


def get_user(username: str) -> UserInDB | None:
    """Поиск пользователя в базе данных"""
    for user in fake_db:
        if compare_digest(user.username, username):
            return user
    return None

def add_user(username: str, password: str) -> UserInDB:
    """Добавление пользователя в базу данных"""
    hashed_password = hash_password(password)
    new_user = UserInDB(username=username, hashed_password=hashed_password)
    fake_db.append(new_user)
    return new_user
    
def auth_user(username: str, password: str) -> bool:
    """Проверка авторизации пользователя"""
    user_in_db = get_user(username)
    if user_in_db and verify_password(password, user_in_db.hashed_password):
        return True
    return False