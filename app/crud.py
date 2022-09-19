from sqlalchemy.orm import Session
import yfinance, requests
import pandas as pd
from typing import List
from . import models, schemas, utils

def get_cpi(db: Session, limit: int = 12 * 2) -> List[schemas.cpi]:
    data = db.query(models.cpi)
    if not data.count():
        return set_cpi(db, limit)
    return data.all()[::-1][:limit]

def set_cpi(db: Session, limit: int = 12 * 2) -> List[schemas.cpi]:
    data = utils.get_cpi_data(model=models.cpi)
    db.bulk_save_objects(data)
    db.commit()
    return data[::-1][:limit]

def get_dxy(db: Session, limit: int = 365 * 2) -> List[schemas.dxy]:
    data = db.query(models.dxy)
    if not data.count():
        return set_dxy(db, limit)
    return data.all()[::-1][:limit]

def set_dxy(db: Session, limit: int = 365 * 2) -> List[schemas.dxy]:
    data = utils.get_yfinance_data(ticker='DX-Y.NYB', period='max', model=models.dxy)
    db.bulk_save_objects(data)
    db.commit()
    return data[::-1][:limit]

def get_spy(db: Session, limit: 365 * 2) -> List[schemas.spy]:
    data = db.query(models.spy)
    if not data.count():
        return set_spy(db, limit)
    return data.all()[::-1][:limit]

def set_spy(db: Session, limit: 365 * 2) -> List[schemas.spy]:
    data = utils.get_yfinance_data(ticker='SPY', period='max', model=models.spy)
    db.bulk_save_objects(data)
    db.commit()
    return data[::-1][:limit]

def get_dji(db: Session, limit: 365 * 2) -> List[schemas.dji]:
    data = db.query(models.dji)
    if not data.count():
        return set_dji(db, limit)
    return data.all()[::-1][:limit]

def set_dji(db: Session, limit: 365 * 2) -> List[schemas.dji]:
    data = utils.get_yfinance_data(ticker='DJI', period='max', model=models.dji)
    db.bulk_save_objects(data)
    db.commit()
    return data[::-1][:limit]