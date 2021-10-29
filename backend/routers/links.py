from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT

from sqlalchemy.orm import Session
from ..mysql import models
from ..mysql import database

router = APIRouter()

@router.get(path="/links_one/")
def links_one(
        Authorize: AuthJWT = Depends(),
        db: Session = Depends(database.get_db)
    ):

    Authorize.jwt_required()

    result = db.query(models.Links).first()
    print(result)

    if result is None:
        raise HTTPException(status_code=404, detail="ID에 해당하는 links가 없습니다.")

    return {
        "status": "OK",
        "data": result
    }


@router.get(path="/links_10/")
def links_10(
        Authorize: AuthJWT = Depends(),
        db: Session = Depends(database.get_db)
    ):

    Authorize.jwt_required()

    result = db.query(models.Links).limit(10).all()
    print(len(result))

    if result is None:
        raise HTTPException(status_code=404, detail="ID에 해당하는 links가 없습니다.")

    return {
        "status": "OK",
        "data": result
    }