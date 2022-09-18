from fastapi import FastAPI, Depends, Request, HTTPException
from .database import engine, get_db
from sqlalchemy.orm import Session
from . import schemas, models, crud
from typing import List

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.middleware("http")
async def add_no_cache_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache"
    return response

@app.get('/')
def index():
    return {'name': 'Hello FastAPI!'}

@app.get('/cpi', response_model=List[schemas.cpi])
def get_cpi(limit: int = 12, update: bool = False, db: Session = Depends(get_db)):
    if update:
        db.query(models.cpi).delete()
        return crud.set_cpi(db, limit=limit)
    return crud.get_cpi(db, limit=limit)

@app.get('/dxy', response_model=List[schemas.dxy])
def get_dxy(limit: int = 365, update: bool = False, db: Session = Depends(get_db)):
    if update:
        db.query(models.dxy).delete()
        return crud.set_dxy(db, limit=limit)
    return crud.get_dxy(db, limit=limit)