# from fastapi import FastAPI, Request
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from fastapi_jwt_auth import AuthJWT

from sqlalchemy.orm import Session
from ..mysql import models
from ..mysql import database

from ..util import userData

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get(path="/", response_class=HTMLResponse)
async def home(request: Request, Authorize: AuthJWT = Depends(), db: Session = Depends(database.get_db)):
    try:
        Authorize.jwt_required()
        email_adress = Authorize.get_jwt_subject()
        context={}
        context["request"] = request
        context["data"] = db.query(models.GameUser).filter(models.GameUser.email_adress == email_adress).first()
        
        # context["data"] = userData.asf(db)
        # {% for ml in data %}
        # <li> {{ ml.content }} </li>
        # {% endfor %}
        return templates.TemplateResponse("index.html", context)
    except Exception as e:
        context={}
        context["request"] = request
        context["notice"] = "로그인 실패"
        return templates.TemplateResponse("login.html", context)

# 로그인 시, 다시 홈으로 돌아가는 거임.
@router.post(path="/", response_class=HTMLResponse)
async def home_post(request: Request):
    context={}
    context["request"] = request
    return RedirectResponse(url="/", status_code=302)





@router.get(path="/register", response_class=HTMLResponse)
async def register(request: Request):
    context={}
    context["request"] = request
    return templates.TemplateResponse("register.html", context)

@router.post(path="/register", response_class=HTMLResponse)
async def create_user(
        email_adress: str = Form(...),
        password: str = Form(...),
        username: str = Form(...),
        db: Session = Depends(database.get_db)):

    print(email_adress, password, username)
    user = models.GameUser()
    user.email_adress = email_adress
    user.password = password
    user.username = username

    db.add(user)
    db.commit()

    return RedirectResponse(url="/register", status_code=302)