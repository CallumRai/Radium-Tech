from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import requests


class Equity:
    def __init__(self, symbol, start_date, end_date, key):
        """
        Object for single equity

        Args:
            symbol: Symbol of equity
            start_date: First day of interest
            end_date: Last day of interest
            key: Alpha-vantage API-Key
        """

        # Convert dates from strings to date objects
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        # Raises error if date range invalid
        if end_date <= start_date:
            raise Exception("End date same as or before start date")

        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.key = key

        # Fetch all data
        df = self._daily()

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

    def _daily(self):

        """
        Gets all available daily signals from an equity

        Args:
            equity: Equity to get data from

        Returns: Dataframe of  daily signals
        """

        # Get signals in JSON form
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={self.symbol}&apikey={self.key}" \
              f"&outputsize=full"
        json = requests.get(url).json()

        # Put JSON into a pandas dataframe, if error API call limit increased
        try:
            daily_json = json["Time Series (Daily)"]
        except KeyError:
            raise RuntimeError("API key invalid or API call limit reached, try again in 1 minute.")

        df = pd.DataFrame(daily_json).T

        # Format data as numerical
        columns = list(df.columns)
        for col in columns:
            df[col] = pd.to_numeric(df[col])

        # Format index as a date
        df.index = pd.to_datetime(df.index).date

        return df

    def plot(self, start_date=None, end_date=None):
        """
        Plots closed prices of equity between two dates

        Args:
            start_date: First date to plot (default: start_date)
            end_date: Last date to plot (default: end_date)

        Returns: None

        """
        # If no start/end date specified use default
        if start_date is None:
            start_date = self.start_date
        else:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

        if end_date is None:
            end_date = self.end_date
        else:
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        # Raises error if date range invalid
        if end_date <= start_date:
            raise Exception("End date same as or before start date")

        # Gets required range only
        closed = self.closed
        mask = (closed.index >= start_date) & (closed.index <= end_date)
        closed = closed.loc[mask]

        fig, ax = plt.subplots()
        ax.plot(closed)

        plt.title(f"{self.symbol} from {start_date} to {end_date}")
        plt.xlabel("Date")
        plt.ylabel("Adjusted closed prices ($)")

        # Put dollar marks infront of y axis
        formatter = ticker.FormatStrFormatter('$%1.2f')
        ax.yaxis.set_major_formatter(formatter)

        plt.grid()
        plt.show()
