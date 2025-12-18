import yfinance as yf
import pandas as pd
import os

def scrape_stock_prices(symbols, output_path="stocks.csv"):
    """Scrape stock prices for given symbols and save to CSV.
    Args:
        symbols (list): List of stock symbols (str)
        output_path (str): Path to save the CSV file
    Returns:
        str: Path to the saved CSV file
        pd.DataFrame: DataFrame containing stock prices
    """
    data = {s: yf.Ticker(s).info.get("regularMarketPrice", None) for s in symbols}
    df = pd.DataFrame(list(data.items()), columns=["Symbol", "Price"])
    df.to_csv(output_path, index=False)
    return output_path, df