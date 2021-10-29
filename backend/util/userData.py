from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from ..mysql import models
from ..mysql import database

def asf(db):
    # res = db.query(models.Links).first()
    res = db.query(models.Links).limit(10).all()
    return res
