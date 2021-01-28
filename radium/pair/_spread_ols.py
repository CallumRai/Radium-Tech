import numpy as np
import pandas as pd
import statsmodels.tsa.stattools as ts


def _spread_ols(self, lookback):
    """
    Args:
        self: Pair of equities
        lookback: Number of prev. signals to lookback on when regressing ols (for hedge ratios

    Returns: Price spread of pair

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