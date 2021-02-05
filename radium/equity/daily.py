import pandas as pd
import requests


def daily(equity):
    """
    Args:
        equity

    Returns: Dataframe of all available daily signals

    """
    # Get signals in JSON form
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={equity.symbol}&apikey={equity.key}" \
          f"&outputsize=full"
    json = requests.get(url).json()

    # Put JSON into a pandas dataframe, if error API call limit increased
    try:
        daily_json = json["Time Series (Daily)"]
    except KeyError:
        raise Exception("API call limit reached, try again in 1 minute.")
    df = pd.DataFrame(daily_json).T

    # Format data as numerical
    columns = list(df.columns)
    for col in columns:
        df[col] = pd.to_numeric(df[col])

    # Format index as a date
    df.index = pd.to_datetime(df.index).date

    return df
