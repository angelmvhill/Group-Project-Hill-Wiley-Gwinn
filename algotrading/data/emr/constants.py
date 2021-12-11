import os
import pathlib

BUCKET = r"s3://firstratedata/"

STOCKS_BASE = BUCKET + r"us_stocks/"
CRYPTO_BASE = BUCKET + r'crypto/'
INDICES_BASE = BUCKET + r'indices/'
FUTURES_BASE = BUCKET + r'futures/'
ETFS_BASE = BUCKET + r'etfs/'
FX_BASE = BUCKET + r'fx/'

# US Stocks
STOCKS_1_MINUTE = {
    'txt': STOCKS_BASE+r'1_minute/',
    'txt_unadj': STOCKS_BASE+r'1_minute_unadj/',
    'csv': STOCKS_BASE + r'1_minute_csv/',
    'parquet': STOCKS_BASE + r'1_minute_parquet/'
}
STOCKS_5_MINUTES = STOCKS_BASE + r'5_minutes/'
STOCKS_30_MINUTES = STOCKS_BASE + r'30_minutes/'
STOCKS_1_HOUR = STOCKS_BASE + r'1_hour/'

# Crypto
CRYPTO_1_MINUTE = CRYPTO_BASE + r'1_minute/'
CRYPTO_5_MINUTES = CRYPTO_BASE + r'5_minutes/'
CRYPTO_30_MINUTES = CRYPTO_BASE + r'30_minutes/'
CRYPTO_1_HOUR = CRYPTO_BASE + r'1_hour/'

# US Indices
INDICES_1_MINUTE = INDICES_BASE + r'1_minute/'
INDICES_5_MINUTES = INDICES_BASE + r'5_minutes/'
INDICES_30_MINUTES = INDICES_BASE + r'30_minutes/'
INDICES_1_HOUR = INDICES_BASE + r'1_hour/'

# Futures
FUTURES_1_MINUTE = FUTURES_BASE + "1_minute/"
FUTURES_5_MINUTES = FUTURES_BASE + r'5_minutes/'
FUTURES_30_MINUTES = FUTURES_BASE + r'30_minutes/'
FUTURES_1_HOUR = FUTURES_BASE + r'1_hour/'
FUTURES_INDIVIDUAL_CONTRACTS = FUTURES_BASE + r'individual_contracts/'

# ETFS
ETFS_1_MINUTE = ETFS_BASE + r'1min/'
ETFS_1_MINUTE_UNADJ = ETFS_BASE + r'1_minute_unadj/'
ETFS_5_MINUTES = ETFS_BASE + r'5_minutes/'
ETFS_30_MINUTES = ETFS_BASE + r'30_minutes/'
ETFS_1_HOUR = ETFS_BASE + r'1_hour/'

# FX
FX_1_MINUTE = FX_BASE + r'1_minute/'
FX_5_MINUTES = FX_BASE + r'5_minutes/'
FX_30_MINUTES = FX_BASE + r'30_minutes/'
FX_1_HOUR = FX_BASE + r'1_hour/'


# First Rate Data Schema

STOCKS_SCHEMA = "datetime string "