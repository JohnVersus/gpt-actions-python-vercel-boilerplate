from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from .routes import router as BookRouter

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", tags=["Root"])
async def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Chat GPT Plugin FastAPI",
            "description": "ChatGPT Plugin API build using FastAPI and for hosting on vercel.",
            "message": "ChatGPT Plugin API build using FastAPI and hosted on vercel.",
        },
    )


app.include_router(BookRouter, prefix="/book")
