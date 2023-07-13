from fastapi.responses import HTMLResponse
from os import listdir
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def get_static_files(request: Request):
    files = listdir("static")
    return templates.TemplateResponse(
        "files.html", {"request": request, "files": files}
    )
