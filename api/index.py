from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from urllib.parse import unquote, urlparse
from .database import Session, APIRequest  # Importing the database session and model
from . import BookRouter, StaticRouter, generate_plugin_info_file
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")  # Retrieving the token from environment variables
security = HTTPBearer()  # Bearer token-based security


# Token verification function
async def verify_token(token: HTTPAuthorizationCredentials = Depends(security)):
    if token.credentials != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key"
        )
    return token.credentials


# Middleware for logging to database
class DBLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        request.state.db = Session()
        response_status = None
        try:
            response = await call_next(request)
            response_status = response.status_code
        except Exception as e:
            response_status = 500
        finally:
            if str(request.url.path) in app.openapi().get("paths"):
                api_request = APIRequest(
                    host=request.headers.get("host"),
                    real_ip=request.headers.get("x-real-ip"),
                    user_id=request.headers.get("openai-ephemeral-user-id"),
                    conversation_id=request.headers.get("openai-conversation-id"),
                    subdivision_code=request.headers.get(
                        "openai-subdivision-1-iso-code"
                    ),
                    endpoint=urlparse(request.url.path).path,
                    query_parameters=unquote(request.url.query),
                    response_status=response_status,
                )
                request.state.db.add(api_request)
                request.state.db.commit()
            request.state.db.close()
        return response


app = FastAPI(
    title="Bookstore API", description="ChatGPT Plugin API docs", version="0.0.1"
)

# uncomment to save on db
# app.add_middleware(DBLoggerMiddleware)  # Add the middleware

templates = Jinja2Templates(directory="templates")


@app.get("/", tags=["Root"], include_in_schema=False)
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


# Protect routers with the verify_token dependency
app.include_router(BookRouter, prefix="/book", dependencies=[Depends(verify_token)])
app.include_router(
    StaticRouter,
    prefix="/static",
    dependencies=[Depends(verify_token)],
    include_in_schema=False,
)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/.well-known/ai-plugin.json", include_in_schema=False)
async def serve_plugin_info():
    return generate_plugin_info_file()
