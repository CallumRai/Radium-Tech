import statsmodels.tsa.stattools as ts
import statsmodels.formula.api as sm
from .johansen_test import *
import numpy as np
from radium.helpers import *
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

class Pair:
    def __init__(self, equity1, equity2):
        """
        Object for pair of equities.

        Args:
            equity1: First equity in pair, will be used as response variable when regressing
            equity2: Second equity in pair
        """

        self.equity1 = equity1
        self.equity2 = equity2
        self.start_date = equity1.start_date
        self.end_date = equity1.end_date

    def hedge_ols(self, lookback):
        """
        Estimates hedge ratios of equities by OLS regression

        Args:
            lookback: Number of signals to lookback on when regressing

        Returns: Hedge ratios as 2D array
        """

        # Construct dataframe of closed prices
        df = pd.concat([self.equity1.closed, self.equity2.closed], axis=1)
        df.columns = [self.equity1.symbol, self.equity2.symbol]

        # Get ols regression result for each date
        hedge_ratio = np.full(df.shape[0], np.nan)
        for i in range(lookback, len(hedge_ratio)):
            formula = f"{self.equity1.symbol} ~ {self.equity2.symbol}"
            df_lookback = df[(i - lookback):i]
            ols = sm.ols(formula, df_lookback).fit()

            # Hedge ratio for date is ols gradient
            hedge_ratio[i - 1] = ols.params[1]

        return hedge_ratio

    def spread_ols(self, lookback):
        """
        Estimates spread of equities by OLS regression

        Args:
            lookback: Number of signals to lookback on when regressing

        Returns: Price spread as 2D array
        """

        # Construct dataframe of closed prices
        df = pd.concat([self.equity1.closed, self.equity2.closed], axis=1)
        df.columns = [self.equity1.symbol, self.equity2.symbol]

        hedge_ratio = self.hedge_ols(lookback)
        # create matrix of 1s and -h to element-wise multiply with close data for spread (y = y1 - hy2)
        hedge_matrix = ts.add_constant(-hedge_ratio)
        # multiply and add for each date
        spread = np.sum(hedge_matrix * df, axis=1)

        return spread

    def budget(self):
        """
        Prints budget to varying decimal places.

        Returns: None
        """

        # Get the prices at end_date
        equity1_price = self.equity1.closed.iloc[0]
        equity2_price = self.equity2.closed.iloc[0]

        # Calculate theoretical ratios
        ratios_th = johansen_test(self)

        # Calculate ratios to 4 decimal places, 3 d.p., ..., 1 d.p
        ratios_4dp = np.array([truncate(n, 4) for n in ratios_th])
        ratios_3dp = np.array([truncate(n, 3) for n in ratios_th])
        ratios_2dp = np.array([truncate(n, 2) for n in ratios_th])
        ratios_1dp = np.array([truncate(n, 1) for n in ratios_th])

        # Calculate budgets for 4 dp, 3 dp, ..., 1 dp
        budget_4dp = equity1_price * ratios_4dp[0] * 10000 + equity2_price * ratios_4dp[1] * 10000
        budget_3dp = equity1_price * ratios_3dp[0] * 1000 + equity2_price * ratios_3dp[1] * 1000
        budget_2dp = equity1_price * ratios_2dp[0] * 100 + equity2_price * ratios_2dp[1] * 100
        budget_1dp = equity1_price * ratios_1dp[0] * 10 + equity2_price * ratios_1dp[1] * 10

        return [budget_1dp, budget_2dp, budget_3dp, budget_4dp]

    def plot(self, start_date=None, end_date=None):
        """
        Plots closed prices of both equities between two dates

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

        # Gets required range only for both equities
        equity1_closed = self.equity1.closed
        mask = (equity1_closed.index >= start_date) & (equity1_closed.index <= end_date)
        equity1_closed = equity1_closed.loc[mask]

        equity2_closed = self.equity2.closed
        mask = (equity2_closed.index >= start_date) & (equity2_closed.index <= end_date)
        equity2_closed = equity2_closed.loc[mask]

        fig, ax = plt.subplots()
        plt.plot(equity1_closed, label = self.equity1.symbol)
        plt.plot(equity2_closed, label = self.equity2.symbol)

        plt.title(f"{self.equity1.symbol} and {self.equity2.symbol} from {start_date} to {end_date}")
        plt.xlabel("Date")
        plt.ylabel("Adjusted closed prices ($)")

        # Put dollar marks infront of y axis
        formatter = ticker.FormatStrFormatter('$%1.2f')
        ax.yaxis.set_major_formatter(formatter)

        plt.legend()
        plt.grid()
        plt.show()
