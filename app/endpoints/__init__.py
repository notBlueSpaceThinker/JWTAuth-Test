from fastapi import FastAPI

from . import docs, login


def include_routers(app: FastAPI) -> None:
    app.include_router(login.router)
    app.include_router(docs.router)
