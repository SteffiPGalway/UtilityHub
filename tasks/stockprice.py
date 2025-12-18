import yfinance as yf

def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    return stock.history(period="1d")["Close"]
