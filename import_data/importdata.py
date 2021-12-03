import numpy as np
import pandas as pd
# import yfinance as yf
# import yfinance.stock_info as si
import backtrader as bt

df_stock = pd.read_csv(r"data/AAPL.csv")
df_fin = pd.read_csv(r"data/AAPLfinancials.csv")
print(df_stock)
print(df_fin)

# step 2: merge datasets together - the datasets need to be merged together
# need to add a column that adds does a running calculation of current PE ratio based on price
# make sure that dates line up between PE ratios and time series data
# make sure that the PE ratio changes every quarter




# aapl_data = si.get_quote_table("MSFT")
# print(aapl_data)

# apple = yf.Ticker('aapl')
# print(apple)

# print((apple.info['trailingPE']))

# http://financials.morningstar.com/ratios/r.html?t=AAPL&region=usa&culture=en-US
# link for earnings data csv\

# https://stockrow.com/AAPL/financials/income/quarterly
# better link for earnings data (quarterly instead of annually)