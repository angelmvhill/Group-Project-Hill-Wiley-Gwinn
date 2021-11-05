import numpy as np
import pandas as pd
import yfinance as yf
# import yfinance.stock_info as si

df_stock = pd.read_csv(r"data/AAPL.csv")
df_fin = pd.read_csv (r"data/AAPLfinacials.csv")
# print(df)

# aapl_data = si.get_quote_table("MSFT")
# print(aapl_data)

apple = yf.Ticker('aapl')
# print(apple)

print((apple.info['trailingPE']))

# http://financials.morningstar.com/ratios/r.html?t=AAPL&region=usa&culture=en-US
# link for earnings data csv\

# https://stockrow.com/AAPL/financials/income/quarterly
# better link for earnings data (quarterly instead of annually)