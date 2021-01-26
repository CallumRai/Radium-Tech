from datetime import datetime, timedelta
import pandas as pd
import requests


def daily_df(symbol, key):
    """
    :param symbol: Name of equity
    :param key: API key
    :return: Dataframe of all daily equity signals
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
    adj_clo_df = adj_clo_df.iloc[:, 4].to_frame()

    return adj_clo_df


def fill_missing_date(df):
    """
    :param df: Dataframe of a set of stocks
    :return: Missing prices filled with previous
    """

    # get list of required dates
    s_date = df.index[-1]
    e_date = df.index[0]
    days = list(pd.date_range(s_date, e_date))
    days = [d.date() for d in days]

    # initialise full dataframe
    days_df = pd.DataFrame(index = days)
    # augment dataset
    full_df = pd.concat([days_df, df], axis=1)

    # iterate through each possibly empty cell
    for i in range(1, len(full_df.index)):
        for j in range(len(full_df.columns)):
            cell = full_df.iat[i, j]

            # replace cell if empty
            if pd.isna(cell):
                full_df.iat[i, j] = full_df.iat[i - 1, j]

    return full_df
