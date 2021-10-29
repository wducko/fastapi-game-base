from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi_jwt_auth import AuthJWT
from starlette.responses import RedirectResponse
from pydantic import BaseModel

from sqlalchemy.orm import Session
from ..mysql import models
from ..mysql import database

from .web import templates

router = APIRouter()

class GameUser(BaseModel):
  email_adress: str
  password: str

@router.post('/login')
def login(
        request: Request,
        user: GameUser,
        Authorize: AuthJWT = Depends(), 
        db: Session = Depends(database.get_db)
    ):

    userrr = db.query(models.GameUser)\
               .filter(models.GameUser.email_adress == user.email_adress)\
               .filter(models.GameUser.password == user.password)\
               .first()
    if userrr == None:
        context={}
        context["request"] = request
        context["notice"] = "로그인 정보 틀림"
        return templates.TemplateResponse("login.html", context)

    # Create the tokens and passing to set_access_cookies or set_refresh_cookies
    access_token = Authorize.create_access_token(subject=user.email_adress)
    refresh_token = Authorize.create_refresh_token(subject=user.email_adress)

    # Set the JWT and CSRF double submit cookies in the response
    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    return {"status": 200, "msg":"Successfully login"}

@router.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    # Set the JWT and CSRF double submit cookies in the response
    Authorize.set_access_cookies(new_access_token)
    return {"status": 200, "msg":"The token has been refresh"}

@router.get('/logout')
def logout(Authorize: AuthJWT = Depends()):
    """
    Because the JWT are stored in an httponly cookie now, we cannot
    log the user out by simply deleting the cookie in the frontend.
    We need the backend to send us a response to delete the cookies.
    """
    Authorize.jwt_required()

    Authorize.unset_jwt_cookies()
    return {"status": 200, "msg":"Successfully logout"}

@router.get('/protected')
def protected(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}