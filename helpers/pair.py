import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as sm
import statsmodels.tsa.stattools as ts
import statsmodels.tsa.vector_ar.vecm as vm

class Pair:
    def __init__(self, equity1, equity2):
        self.equity1 = equity1
        self.equity2 = equity2

    def hedge_ols(self, lookback):
        """
        :param lookback: Number of prev. signals to lookback over when calculating ols coeff.
        :return: OLS estimate of hedge ratio for each date w/ first pair as response
        """

        # Construct dataframe of closed prices
        df = pd.concat([self.equity1.closed, self.equity2.closed], axis=1)
        df.columns = [self.equity1.symbol, self.equity2.symbol]

        # Get ols regression result for each date
        hedge_ratio = np.full(df.shape[0], np.nan)
        for i in range(lookback, len(hedge_ratio)):
            formula = f"{self.equity1.symbol} ~ {self.equity2.symbol}"
            df_lookback = df[(i-lookback):i]
            ols = sm.ols(formula, df_lookback).fit()

            # Hedge ratio for date is ols gradient
            hedge_ratio[i-1] = ols.params[1]

        return hedge_ratio

    def spread_ols(self, lookback):
        """
        :param lookback: Number of prev. signals to lookback over when estimating hedge ratio
        :return: Spread using OLS estimate of hedge ratio w/ first pair as response
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