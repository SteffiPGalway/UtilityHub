from forex_python.converter import CurrencyRates

def convert_currency(amount, from_currency, to_currency):
    c = CurrencyRates()
    try:
        return c.convert(from_currency, to_currency, amount)
    except Exception:
        # retry once
        c = CurrencyRates(force_refresh=True)
        return c.convert(from_currency, to_currency, amount)
