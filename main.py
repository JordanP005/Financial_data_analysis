#import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

load_dotenv()

fred_key = os.getenv("FRED_KEY")

NDX_price = yf.download(tickers="^NDX",interval="1D", start="2020-01-01", end="2025-12-31")
NDX_df = pd.DataFrame(NDX_price)

NDX_df['return'] = NDX_df['Close'].pct_change()
NDX_df.dropna(inplace=True)
NDX_df.columns = NDX_df.columns.get_level_values(0)
NDX_df.columns.name = None
NDX_df = NDX_df.reset_index()
NDX_df = NDX_df.set_index("Date")

print(NDX_df)

# LABOR       → PAYEMS        (NFP, monthly, BLS)
# INFLATION_1 → CPIAUCSL      (CPI, monthly, BLS)
# INFLATION_2 → PCEPILFE      (Core PCE, monthly, BEA)
# MONETARY    → FEDFUNDS      (FOMC decision, 8x/year, Fed)
# CONSUMPTION → RSXFS         (Retail Sales, monthly, Census)
# INVESTMENT  → DGORDER       (Durable Goods, monthly, Census)
# GDP         → GDP           (Advance release, quarterly, BEA)

from fredapi import Fred
print(f'fred:{fred_key}')
fred = Fred(api_key=f'{fred_key}')

SERIES_df = pd.DataFrame(fred.get_series('PAYEMS', observation_start="2020-01-01", observation_end="2025-12-31"))
SERIES_df.index.name ='Date'
SERIES_df = SERIES_df.resample("D").ffill()
print(SERIES_df)

NDX_df = NDX_df.join(SERIES_df, lsuffix="_price", rsuffix="_other")

print(NDX_df)

NDX_df.plot()
plt.show()