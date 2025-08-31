from fastapi import FastAPI


from . import login, docs


def include_routers(app: FastAPI) -> None:
    app.include_router(login.router)
    app.include_router(docs.router)