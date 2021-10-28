from pydantic.main import BaseModel

from fastapi import FastAPI, Depends, Path, HTTPException
from sqlalchemy.orm import Session
from . import models
from . import database

class HelloWorldRequest(BaseModel):
    name: str
    age: int

app = FastAPI()

@app.get(path="/")
async def hello():
    return "hello world" 

@app.get(path="/hello/{name}")
async def hello_with_name(name: str):
    return "hello with name. your name is " + name

@app.get(path="/hello/query/")
async def hello_with_querystring(name: str):
    return "hello with name. your name is " + name

@app.post(path="/hello/post")
async def hello_post(request: HelloWorldRequest):
    return "hello with post. your name: {}, your age: {}".format(request.name, request.age)

@app.get(path="/api/v1/users/{user_id}")
def get_place(
        user_id: int,
        db: Session = Depends(database.get_db)):
    result = db.query(models.User).filter(models.User.id == user_id).first()

    if result is None:
        raise HTTPException(status_code=404, detail="ID에 해당하는 User가 없습니다.")

    return {
        "status": "OK",
        "data": result
    }

@app.get(path="/api/v1/links/")
def get_links(
        db: Session = Depends(database.get_db)):
    result = db.query(models.Links).first()
    print(len(result))

    if result is None:
        raise HTTPException(status_code=404, detail="ID에 해당하는 links가 없습니다.")

    return {
        "status": "OK",
        "data": result
    }


@app.get(path="/api/v1/links2/")
def get_links(
        db: Session = Depends(database.get_db)):
    result = db.query(models.Links).limit(10).all()
    print(len(result))

    if result is None:
        raise HTTPException(status_code=404, detail="ID에 해당하는 links가 없습니다.")

    return {
        "status": "OK",
        "data": result
    }