import yfinance as yf
import time

def get_stock_price(ticker, retries=3):
    for i in range(retries):
        try:
            df = yf.download(ticker, period="1d", progress=False)
            return df["Close"].iloc[-1]
        except Exception:
            time.sleep(2 ** i)
    return None
