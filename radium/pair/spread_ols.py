import numpy as np
import pandas as pd
import statsmodels.tsa.stattools as ts
from .hedge_ols import hedge_ols

def spread_ols(pair, lookback):
    """
    Args:
        pair: Pair of equities
        lookback: Number of prev. signals to lookback on when regressing ols (for hedge ratios

    Returns: Price spread of pair

    """

    # Construct dataframe of closed prices
    df = pd.concat([pair.equity1.closed, pair.equity2.closed], axis=1)
    df.columns = [pair.equity1.symbol, pair.equity2.symbol]

    hedge_ratio = hedge_ols(pair, lookback)
    # create matrix of 1s and -h to element-wise multiply with close data for spread (y = y1 - hy2)
    hedge_matrix = ts.add_constant(-hedge_ratio)
    # multiply and add for each date
    spread = np.sum(hedge_matrix * df, axis=1)

    return spread