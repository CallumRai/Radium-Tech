from datetime import datetime
import pandas as pd
import requests


def daily_df(symbol, key):
    """
    :param symbol: Name of equity
    :param key: API key
    :return: Dataframe of all daily stock signals
    """

    # Get signals in JSON form
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={key}&" \
          f"outputsize=full"
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


def adjusted_closed(symbol, start_date, end_date, key):
    """
    :param symbol: Name of equity
    :param start_date: First date
    :param end_date: Last date
    :param key: Api key
    :return: Dataframe of the daily adjusted closed price of an equity between two dates
    """

    # format dates
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    # get dataframe of all signals
    full_df = daily_df(symbol, key)

    # get dates of interest only
    mask = (full_df.index >= start_date) & (full_df.index <= end_date)
    adj_clo_df = full_df.loc[mask]

    # get column of interest only (as a dateframe)
    adj_clo_df = adj_clo_df.iloc[:,4].to_frame()

    return adj_clo_df