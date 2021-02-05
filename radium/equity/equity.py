from datetime import datetime
from .daily import daily


class Equity:
    def __init__(self, symbol, start_date, end_date, key):
        """
        Args:
            symbol: Symbol of equity
            start_date: First day of interest
            end_date: Last day of interest
            key: Alpha-vantage API-Key
        """

        # Convert dates from strings to date objects
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.key = key

        # Fetch all data
        df = daily(self)

        # get dates of interest only
        mask = (df.index >= start_date) & (df.index <= end_date)
        df = df.loc[mask]

        # Fill missing data with previous data
        df.fillna(method='ffill')

        # Set data attribute
        self.data = df

        # Set each possible price type
        self.high = df["2. high"]
        self.low = df["3. low"]
        self.open = df["1. open"]
        self.closed = df["5. adjusted close"]