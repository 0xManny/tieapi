import requests
import pandas as pd

# helpful links
# https://download.bls.gov/pub/time.series/cu/cu.txt
# https://download.bls.gov/pub/time.series/cu/

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
df['cpi'] = (df['value'].pct_change(12) * 100).dropna()
df = df[['date', 'cpi']]
print(df)