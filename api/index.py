from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from .app import router as BookRouter
from .static import router as StaticRouter
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(
    title="Bookstore API", description="ChatGPT Plugin API docs", version="0.0.1"
)

templates = Jinja2Templates(directory="templates")


@app.get("/", tags=["Root"])
async def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Chat GPT Plugin API",
            "description": "ChatGPT Plugin API built using FastAPI and for hosting on vercel.",
            "message": "ChatGPT Plugin API build using FastAPI and hosted on vercel.",
        },
    )


app.include_router(BookRouter, prefix="/book")
app.include_router(StaticRouter, prefix="/static", include_in_schema=False )
app.mount("/static", StaticFiles(directory="static"), name="static" )


@app.get("/.well-known/ai-plugin.json", include_in_schema=False )
async def serve_plugin_info():
    return FileResponse("static/ai-plugin.json")
