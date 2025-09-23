from hmac import compare_digest

from app.schemas.user import User, UserInDB
from app.security import hash_password, verify_password

fake_db: list[User] = [
    UserInDB(
        username="test_1",
        full_name="test_name",
        email="mail@test.com",
        roles=["admin", "guest"],
        hashed_password=hash_password("test")
    ),
        UserInDB(
        username="test_2",
        full_name="test_name",
        email="mail@test.com",
        roles=["useless role"],
        hashed_password=hash_password("test")
    )
]


def get_user(username: str) -> UserInDB | None:
    for user in fake_db:
        if compare_digest(user.username, username):
            return user
    return None


def add_user(
        username: str,
        password: str,
        full_name: str | None = None,
        email: str | None = None,
        disabled: str | None = None,
        roles: list[str] = ["guest"]
        ) -> UserInDB:

    hashed_password = hash_password(password)
    new_user = UserInDB(
        username=username,
        hashed_password=hashed_password,
        full_name=full_name,
        email=email,
        disabled=disabled,
        roles=roles
        )

    fake_db.append(new_user)
    return new_user


def auth_user(username: str, password: str) -> bool:
    user_in_db = get_user(username)
    if user_in_db and verify_password(password, user_in_db.hashed_password):
        return True
    return False


def grand_permission(username: str, roles: list[str]) -> bool:
    user_in_db = get_user(username)
    if not user_in_db:
        return False

    user_in_db.roles.extend(roles)
    return True
