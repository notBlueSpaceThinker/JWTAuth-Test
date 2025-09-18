import uvicorn
from fastapi import FastAPI

from app.endpoints import include_routers

app = FastAPI()
include_routers(app)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
