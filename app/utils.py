import yfinance, requests
import pandas as pd
from fredapi import Fred
from dotenv import load_dotenv
import os

found_env = load_dotenv('.env')
if not found_env:
    raise Exception('Environment could not be found')

fred = Fred(api_key=os.environ['FRED_KEY'])


def get_yfinance_data(ticker, period, model):
    name = model.__tablename__
    t = yfinance.Ticker(ticker)
    t.df = t.history(period=period).reset_index()
    t.df[name] = t.df[['Open','High','Low','Close']].mean(axis=1)
    t.df = t.df[['Date',name]]
    t.df.columns = ['date',name]
    t.data = []
    for index, row in t.df.iterrows():
        t.data.append(model(**{
            'date':int(row['date'].timestamp()),
            name:row[name]
        }))
    return t.data

def get_cpi_data(model):
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
        data.append(model(
            date=int(pd.Timestamp(row['date']).timestamp()),
            cpi=row['cpi']
        ))
    return data

def get_fred_data(series, model):
    name = model.__tablename__
    df = fred.get_series(series)
    df = df.reset_index()
    df.columns = ['date', name]
    data = []
    for index, row in df.iterrows():
        data.append(model(**{
            'date':int(pd.Timestamp(row['date']).timestamp()),
            name:row[name]
        }))
    return data
