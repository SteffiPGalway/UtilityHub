import yfinance as yf
import pandas as pd
import os

def scrape_stock_prices(symbols, output_path="stocks.csv"):
    data = {s: yf.Ticker(s).info.get("regularMarketPrice", None) for s in symbols}
    df = pd.DataFrame(list(data.items()), columns=["Symbol", "Price"])
    df.to_csv(output_path, index=False)
    return output_path, df