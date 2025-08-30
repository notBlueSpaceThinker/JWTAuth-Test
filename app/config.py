from dataclasses import dataclass
from environs import Env

@dataclass
class TokenConfig:
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
def load_token_config(path: str = None) -> TokenConfig:
    env = Env()
    env.read_env(path)

    return TokenConfig(
        SECRET_KEY=env("SECRET_KEY"),
        ALGORITHM=env("ALGORITHM"),
        ACCESS_TOKEN_EXPIRE_MINUTES=env("ACCESS_TOKEN_EXPIRE_MINUTES")
    )