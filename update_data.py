import yfinance as yf
import json
from datetime import datetime, timedelta
import pandas as pd

# Mapping from our display names to Yahoo Finance tickers
INDICES = {
    'SPX': '^GSPC',           # S&P 500
    'NASDAQ': '^IXIC',        # Nasdaq Composite
    'DJI': '^DJI',            # Dow Jones Industrial Average
    'EUROPE': 'VGK',          # Vanguard Europe ETF
    'CHINA': 'MCHI',          # iShares MSCI China ETF
    'JAPAN': 'EWJ',           # iShares MSCI Japan ETF
    'EM': 'VWO',              # Vanguard Emerging Markets ETF
    'DM': 'VEA',              # Vanguard Developed Markets ETF
    'MSCI_WORLD': 'URTH',     # iShares MSCI World ETF
    'MSCI_EXUS': 'ACWX'       # iShares MSCI ACWI ex US ETF
}

print("Fetching global indices data...")

end_date = datetime.now()
start_date = end_date - timedelta(days=365*5 + 30)  # 5 years + buffer

# Download all at once
yf_tickers = list(INDICES.values())
data = yf.download(yf_tickers, start=start_date, end=end_date, progress=True)

result = {}
for display_name, yf_ticker in INDICES.items():
    try:
        if len(INDICES) > 1:
            prices = data['Close'][yf_ticker].dropna()
        else:
            prices = data['Close'].dropna()

        result[display_name] = [
            {"date": date.strftime('%Y-%m-%d'), "price": round(price, 2)}
            for date, price in prices.items()
        ]
        print(f"{display_name}: {len(result[display_name])} days")
    except Exception as e:
        print(f"Error processing {display_name}: {e}")

import os
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stock_data.json')
with open(output_path, 'w') as f:
    json.dump(result, f)

print(f"\nData saved to {output_path}")
if result:
    first_key = list(result.keys())[0]
    print(f"Date range: {result[first_key][0]['date']} to {result[first_key][-1]['date']}")
