from dataclasses import dataclass
from typing import Literal

from environs import Env


@dataclass
class TokenConfig:
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int


def load_token_config(path: str = None) -> TokenConfig:
    env = Env()
    env.read_env(path)

    return TokenConfig(
        SECRET_KEY=env("SECRET_KEY"),
        ALGORITHM=env("ALGORITHM"),
        ACCESS_TOKEN_EXPIRE_MINUTES=env.int("ACCESS_TOKEN_EXPIRE_MINUTES"),
        REFRESH_TOKEN_EXPIRE_MINUTES=env.int("REFRESH_TOKEN_EXPIRE_MINUTES"),
    )


@dataclass
class DocsConfig:
    MODE: Literal["DEV", "PROD"]
    DOCS_USER: str
    DOCS_PASSWORD: str


def load_docs_config(path: str = None) -> DocsConfig:
    env = Env()
    env.read_env(path)

    mode = env("MODE")
    if mode not in ("DEV", "PROD"):
        raise ValueError(f"Invalid MODE: {mode}")

    return DocsConfig(
        MODE=mode,
        DOCS_USER=env("DOCS_USER"),
        DOCS_PASSWORD=env("DOCS_PASSWORD")
    )
