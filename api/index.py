from time import sleep
from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from urllib.parse import unquote, urlparse
from .database import Session, APIRequest  # Importing the database session and model
from . import BookRouter, StaticRouter
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")  # Retrieving the token from environment variables
security = HTTPBearer()  # Bearer token-based security
SERVEL_URL = os.getenv("SERVER_URL", "http://0.0.0.0:8000/")


# Token verification function
async def verify_token(token: HTTPAuthorizationCredentials = Depends(security)):
    if token.credentials != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key"
        )
    return token.credentials


async def save_to_db(session, api_request, retries=1, delay=1):
    for _ in range(retries):
        try:
            session.add(api_request)
            session.commit()
            return True
        except Exception as e:
            print(f"Error logging API request (attempt {_+1}): {e}")
            session.rollback()  # Rollback the session to clean state
            await sleep(delay)  # Delay for a bit before retrying
    return False


class DBLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        request.state.db = Session()
        db_error = False
        response_status = 200  # Default to 200 OK

        try:
            response = await call_next(request)  # Call the actual API endpoint
            response_status = response.status_code
        except Exception as e:
            print(f"API endpoint error: {e}")  # Optionally log the error
            response_status = 500  # Internal Server Error
            response = Response("Internal server error", status_code=500)

        if str(request.url.path) in app.openapi().get("paths"):
            api_request = APIRequest(
                host=request.headers.get("host"),
                real_ip=request.headers.get("x-real-ip"),
                user_id=request.headers.get("openai-ephemeral-user-id"),
                conversation_id=request.headers.get("openai-conversation-id"),
                subdivision_code=request.headers.get("openai-subdivision-1-iso-code"),
                endpoint=urlparse(request.url.path).path,
                query_parameters=unquote(request.url.query),
                response_status=response_status,
            )

            success = await save_to_db(request.state.db, api_request)
            if not success:
                db_error = True

            request.state.db.close()  # Close the session after trying to save to the database

        # If there was a DB error but the API endpoint ran fine, you can decide how to handle this.
        # For instance, you might want to send a custom header or change the response in some way.
        # Below, I've added a custom header for demonstration purposes.
        if db_error:
            response.headers["X-DB-Error"] = "true"

        return response


app = FastAPI(
    title="Bookstore API",
    description="Custome GPT actions API docs",
    version="0.0.1",
    servers=[{"url": SERVEL_URL}],
)

# uncomment to save API requests on db
# app.add_middleware(DBLoggerMiddleware)  # Add the middleware

templates = Jinja2Templates(directory="templates")


@app.get("/", tags=["Root"], include_in_schema=False)
async def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Custome GPT actions API",
            "description": "Custome GPT actions API built using FastAPI and for hosting on vercel.",
            "message": "Custome GPT actions API built using FastAPI and hosted on vercel.",
        },
    )


# Protect routers with the verify_token dependency
app.include_router(BookRouter, prefix="/book", dependencies=[Depends(verify_token)])
app.include_router(
    StaticRouter,
    prefix="/static",
    include_in_schema=False,
)
app.mount("/static", StaticFiles(directory="static"), name="static")
