import yfinance
from pprint import pprint

dxy = yfinance.Ticker('DX-Y.NYB')
dxy.df = dxy.history(period='12mo').reset_index()
dxy.df['dxy'] = dxy.df[['Open','High','Low','Close']].mean(axis=1)
dxy.df = dxy.df[['Date','dxy']]
dxy.df.columns = ['date','dxy']
dxy.df.to_json(orient='records')

pprint(dxy.df[['Date','Price']].to_json(orient='records'))

