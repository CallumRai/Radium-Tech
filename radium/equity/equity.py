from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import requests
from radium.helpers import _convert_date


class Equity:
    """
    Class for a single equity between two dates.

    Attributes
    ----------
    data : pd.DataFrame
        Contains all daily signals with date as index
    high : pd.Series
        Contains daily high prices with date as index
    low : pd.Series
        Contains daily low prices with date as index
    open : pd.Series
        Contains daily open prices with date as index
    closed : pd.Series
        Contains daily adjusted closed prices with date as index
    """

    def __init__(self, symbol, start_date, end_date, key):
        """
        Initialises equity class

        Parameters
        ----------
        symbol : str
            Symbol for equity as found on exchange
        start_date : str or datetime or datetime.date
            First date of interest in YYYY-MM-DD form
        end_date : str of datetime or datetime.date
            Last date of interest in YYYY-MM-DD form
        key : str
            Alpha-vantage API key

        Raises
        ------
        ValueError
            API Key is invalid
            Equity symbol does not exist
            End date is same as or before start date
        RuntimeError
            API Call limit reached
        """

        # Convert dates from strings to date objects
        start_date = _convert_date(start_date)
        end_date = _convert_date(end_date)

        # Raises error if date range invalid
        if end_date <= start_date:
            raise ValueError("end_date is the same as or before start_date")

        # Raises error if key is empty string
        if len(key) == 0:
            raise ValueError("Invalid API Key")

        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.key = key

        # Fetch all data
        df = self._daily()

        # Get dates of interest only
        mask = (df.index >= start_date) & (df.index <= end_date)
        df = df.loc[mask]

        # Sort date earliest first
        df.sort_index(inplace=True)

        # Set data attribute
        self.data = df

        # Set each possible price type
        self.high = df["2. high"]
        self.low = df["3. low"]
        self.open = df["1. open"]
        self.closed = df["5. adjusted close"]

    def _daily(self):
        """
        Gets all available daily signals from an equity between two dates

        Contains open, high, low, close, adjusted close, volume, dividend
        amount, split coefficient, for each day/

        Returns ------- ret : pd.DataFrame Dataframe containing daily signal
        information with date as an index, sorted most recent first.

        Raises
        ------
        ValueError
            Equity symbol does not exist
        RuntimeError
            API Call limit reached
        """

        # Get signals in JSON form
        url = f"https://www.alphavantage.co/query?function" \
              f"=TIME_SERIES_DAILY_ADJUSTED&symbol={self.symbol}" \
              f"&apikey={self.key}" \
              f"&outputsize=full"
        json = requests.get(url).json()

        # Extract signals
        try:
            # If correct data present place time series into list
            daily_json = json["Time Series (Daily)"]
        except KeyError:
            # Test whether an error message is recieved
            try:
                # If error message received from API, incorrect symbol used
                error_json = json["Error Message"]
                raise ValueError("Equity Symbol does not exist")
            except KeyError:
                # Otherwise call limit reached
                raise RuntimeError(
                    "API call limit reached, try again in 1 minute.")

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
        Plots closed prices of equity between two dates as a line graph

        Parameters
        ----------
        start_date : str or datetime or datetime.date
            First date to plot in YYYY-MM-DD form
        end_date : str of datetime or datetime.date
            Last date to plot in YYYY-MM-DD form

        Raises
        ------
        ValueError
            End date is same as or before start date
        """

        # If no start/end date specified use default
        if start_date is None:
            start_date = self.start_date
        else:
            start_date = _convert_date(start_date)

        if end_date is None:
            end_date = self.end_date
        else:
            end_date = _convert_date(end_date)

        # Raises error if date range invalid
        if end_date <= start_date:
            raise ValueError("end_date is the same as or before start_date")

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
