from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.config import load_docs_config

# временная рализация через credentials, а не токен. Пока не выстроена система приоритетов


router = APIRouter()
security = HTTPBasic()

DOCS_CONFIG = load_docs_config()


def hide_doc() -> None:
    """Скрвыает полностью документацию, если включен PROD"""
    if DOCS_CONFIG.MODE == "PROD":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


def auth_doc(credentials: HTTPBasicCredentials = Depends(security)) -> None:
    """Проверка доступка к docs через credentials"""
    if (
        credentials.username == DOCS_CONFIG.DOCS_USER
        and credentials.password == DOCS_CONFIG.DOCS_PASSWORD
    ):
        return None
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={"WWW-Authenticate": "Basic"},
        detail="Invalid credentials",
    )


@router.get(
    "/docs",
    include_in_schema=False,
    dependencies=[Depends(hide_doc), Depends(auth_doc)],
)
async def docs_html():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="API Docs")


@router.get(
    "/openapi.json",
    include_in_schema=False,
    dependencies=[Depends(hide_doc), Depends(auth_doc)],
)
async def openapi_json(request: Request):
    return request.app.openapi()
