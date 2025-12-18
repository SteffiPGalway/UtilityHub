import yfinance as yf
import time

def get_stock_price(ticker, retries=3):
    """Fetch the latest stock price for a given ticker symbol.
    Args:
        ticker (str): Stock ticker symbol
        retries (int): Number of retries in case of failure
    Returns:
        float: Latest stock price or None if failed
    """
    for i in range(retries):
        try:
            df = yf.download(ticker, period="1d", progress=False)
            return df["Close"].iloc[-1]
        except Exception:
            time.sleep(2 ** i)
    return None
