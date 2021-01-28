import numpy as np
import pandas as pd
import statsmodels.formula.api as sm


def _hedge_ols(self, lookback):
    """
    Args:
        self: Pair of equities
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
