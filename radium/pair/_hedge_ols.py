import numpy as np
import pandas as pd
import statsmodels.formula.api as sm


def _hedge_ols(pair, lookback):
    """
    Args:
        pair: Pair of equities
        lookback: Number of prev. signals to lookback on when regressing ols

    Returns: OLS estimate of hedge ratio for each date w/ first equity as response

    """

    # Construct dataframe of closed prices
    df = pd.concat([pair.equity1.closed, pair.equity2.closed], axis=1)
    df.columns = [pair.equity1.symbol, pair.equity2.symbol]

    # Get ols regression result for each date
    hedge_ratio = np.full(df.shape[0], np.nan)
    for i in range(lookback, len(hedge_ratio)):
        formula = f"{pair.equity1.symbol} ~ {pair.equity2.symbol}"
        df_lookback = df[(i - lookback):i]
        ols = sm.ols(formula, df_lookback).fit()

        # Hedge ratio for date is ols gradient
        hedge_ratio[i - 1] = ols.params[1]

    return hedge_ratio
