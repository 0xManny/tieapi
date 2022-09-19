from fredapi import Fred
from dotenv import load_dotenv
import os

found_env = load_dotenv('../.env')
if not found_env:
    raise Exception('Environment could not be found')

fred = Fred(api_key=os.environ['FRED_KEY'])

print(fred.get_series('FEDFUNDS').reset_index())