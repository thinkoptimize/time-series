import yfinance as yf
import pandas as pd
import time
from datetime import datetime


end_date = datetime.today().strftime('%Y-%m-%d')



# Hisse senetlerini, BIST100 endeksi ve USD veri çekme
#tickers = ['USDTRY=X','XU100.IS','FROTO.IS', 'EGEEN.IS', 'ISMEN.IS', 'NUHC.IS', 'GOLTS.IS', 'ERBOS.IS', 'MGROS.IS', 'BIMAS.IS', 'MPARK.IS', 'AKSA.IS', 'TUPRS.IS']
tickers = ['NUHCM.IS']


for ticker in tickers:
    df = yf.download(ticker, start="2021-01-01", end=end_date,auto_adjust=True)
    df.to_excel(f"{ticker}_data.xlsx")
    print(f"{ticker} verisi kaydedildi.")
    time.sleep(2)
