import yfinance
from pprint import pprint

t = yfinance.Ticker('^DJI')
t.df = t.history(period='max').reset_index()
t.df['dji'] = t.df[['Open','High','Low','Close']].mean(axis=1)
t.df = t.df[['Date','dji']]
t.df.columns = ['date','dji']
t.df.to_json(orient='records')

pprint(t.df[['date','dji']].to_json(orient='records'))

