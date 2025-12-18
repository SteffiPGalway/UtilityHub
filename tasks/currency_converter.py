from forex_python.converter import CurrencyRates

def convert_currency(amount, from_currency, to_currency):
    """Convert amount from one currency to another.
    Args:
        amount (float): The amount of money to convert.
        from_currency (str): The currency code to convert from (e.g., 'USD').
        to_currency (str): The currency code to convert to (e.g., 'EUR').
    Returns:
        float: The converted amount."""
    c = CurrencyRates()
    try:
        return c.convert(from_currency, to_currency, amount)
    except Exception:
        # retry once
        c = CurrencyRates(force_refresh=True)
        return c.convert(from_currency, to_currency, amount)
