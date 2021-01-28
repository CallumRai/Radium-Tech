from datetime import datetime

import data


class Equity:
    def __init__(self, symbol, start_date, end_date, key):
        """
        :param symbol: Symbol for equity
        :param start_date: First date of interest
        :param end_date: Last date of interest
        :param key: Alpha-Vantage API key
        """

        # convert dates from strings to date objects
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date

        # Initialise the data

        # Fetch all data
        df = data.daily_df(symbol, key)

        # get dates of interest only
        mask = (df.index >= start_date) & (df.index <= end_date)
        df = df.loc[mask]

        # Fill missing data
        df = data.fill_missing_date(df)

        # Set data attribute
        self.data = df

        # Set each possible price type
        self.high = df["2. high"]
        self.low = df["3. low"]
        self.open = df["1. open"]
        self.closed = df["5. adjusted close"]
z