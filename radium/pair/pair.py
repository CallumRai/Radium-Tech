import statsmodels.tsa.stattools as ts
import statsmodels.formula.api as sm
from .johansen_test import *
import numpy as np
from radium.helpers import *


class Pair:
    def __init__(self, equity1, equity2):
        """
        Pair of equities (note: first equity is used as response variable in ols regression)
        Args:
            equity1: First equity in pair
            equity2: Second equity in pair
        """

        self.equity1 = equity1
        self.equity2 = equity2
        self.start_date = equity1.start_date
        self.end_date = equity1.end_date

    def hedge_ols(self, lookback):
        """
        Args:
            lookback: Number of prev. signals to lookback on when regressing ols

        Returns: OLS estimate of hedge ratio for each date w/ first equity as response

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
        Args:
            lookback: Number of prev. signals to lookback on when regressing ols (for hedge ratios)

        Returns: Price spread of pair

        """

        # Construct dataframe of closed prices
        df = pd.concat([self.equity1.closed, self.equity2.closed], axis=1)
        df.columns = [self.equity1.symbol, self.equity2.symbol]

        hedge_ratio = self.hedge_ols(self, lookback)
        # create matrix of 1s and -h to element-wise multiply with close data for spread (y = y1 - hy2)
        hedge_matrix = ts.add_constant(-hedge_ratio)
        # multiply and add for each date
        spread = np.sum(hedge_matrix * df, axis=1)

        return spread

    def budget(self):
        """

        Returns: Budget to different decimal places

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
