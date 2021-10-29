from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from .routers import web, users, items, links
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

class Settings(BaseModel):
  authjwt_secret_key: str = "secret"
  # Configure application to store and get JWT from cookies
  authjwt_token_location: set = {"cookies"}
  # Disable CSRF Protection for this example. default is True
  authjwt_cookie_csrf_protect: bool = False

@AuthJWT.load_config
def get_config():
  return Settings()

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
  return JSONResponse(
    status_code=exc.status_code,
    content={"detail": exc.message}
  )

app.include_router(web.router,tags=['web'])
app.include_router(users.router,tags=['users'])
app.include_router(items.router,tags=['items'])
app.include_router(links.router,tags=['links'])