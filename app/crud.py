from sqlalchemy.orm import Session
import yfinance, requests
import pandas as pd
from typing import List
from . import models, schemas

def get_cpi(db: Session, limit: int = 12) -> List[schemas.cpi]:
    data = db.query(models.cpi).limit(limit)
    if not data.count():
        return set_cpi(db, limit)
    return data.all()

def set_cpi(db: Session, limit: int = 12) -> List[schemas.cpi]:
    resp = requests.get('https://download.bls.gov/pub/time.series/cu/cu.data.1.AllItems')
    data = [[i.strip() for i in j.split('\t')] for j in resp.text.split('\r\n')]
    df = pd.DataFrame(data[1:], columns=data[0])
    df = df[df['year'].isin([str(i) for i in range(2010, 2024)])]
    df['value'] = df['value'].astype(float)
    # Non-season CPI all items
    # See https://download.bls.gov/pub/time.series/cu/cu.series
    df = df[(df['series_id'] == 'CUUR0000SA0') & (df['period'] != 'M13')]
    df['period'] = df['period'].str.slice(1,3)
    df['date'] = df['period'] + '-' + df['year']
    df['cpi'] = (df['value'].pct_change(12) * 100)
    df.dropna(inplace=True)
    data = []
    for index, row in df.iterrows():
        data.append(models.cpi(
            date=int(pd.Timestamp(row['date']).timestamp()),
            cpi=row['cpi']
        ))
    db.bulk_save_objects(data)
    db.commit()
    return data[:limit]

def get_dxy(db: Session, limit: int = 365) -> List[schemas.dxy]:
    data = db.query(models.dxy).limit(limit)
    if not data.count():
        return set_dxy()
    return data.all()

def set_dxy(db: Session, limit: int = 365) -> List[schemas.dxy]:
    '''
    parameters
        db : Session -> sqlalchemy session object
        limit: int = 365 -> maximum length of returned list
    returns
        list[dict[int, float]] -> date (seconds since epoch) and dxy average price 
    '''
    dxy = yfinance.Ticker('DX-Y.NYB')
    # hard coding '12mo' for now, maybe add as query parameter in future
    dxy.df = dxy.history(period='12mo').reset_index()
    dxy.df['dxy'] = dxy.df[['Open','High','Low','Close']].mean(axis=1)
    dxy.df = dxy.df[['Date','dxy']]
    dxy.df.columns = ['date','dxy']
    dxy.data = []
    for index, row in dxy.df.iterrows():
        dxy.data.append(models.dxy(
            date=int(row['date'].timestamp()),
            dxy=row['dxy']
        ))
    db.bulk_save_objects(dxy.data)
    db.commit()
    return dxy.data[:limit]