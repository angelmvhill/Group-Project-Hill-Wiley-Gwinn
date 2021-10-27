# from alpha_vantage.timeseries import TimeSeries
# from pprint import pprint
# ts = TimeSeries(key='DXFM3JUQQV7C04VC', output_format='pandas')
# data, meta_data = ts.get_intraday(symbol='MSFT',interval='1min', outputsize='full')
# print(data)

# from dotenv import load_dotenv
# load_dotenv(api)
import alpha_vantage
from api import alpha_vantage_api_key
print(earnings(AAPL, alpha_vantage_api_key))