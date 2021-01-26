import numpy as np
import pandas as pd
import statsmodels.tsa.stattools as ts
import matplotlib.pyplot as plt

class BollingerPair():
    def __init__(self, entry_z, exit_z, lookback, pair):
        """
        :param entry_z: Entry Z-score
        :param exit_z: Exit Z-score
        :param lookback: Period to calculate Z-score over
        :param pair: Pair of interest
        """

        # Get pair spread using ols estimate of hedge ratio w/ lookback
        spread = pair.spread_ols(lookback)

        # Calculate Z-score
        spread_mean = spread.rolling(lookback).mean()
        spread_std = spread.rolling(lookback).std()
        spread_z = (spread - spread_mean) / spread_std

        # Calculate long and short entry and exit points
        long_entry = spread_z < - entry_z
        long_exit = spread_z > -entry_z

        short_entry = spread_z > entry_z
        short_exit = spread_z < exit_z

        # Calculate number of units at each point
        units_long = np.zeros(long_entry.shape)
        units_long[:] = np.nan

        units_short = np.zeros(short_entry.shape)
        units_short[:] = np.nan

        units_long[0] = 0
        units_long[long_entry] = 1
        units_long[long_exit] = 0
        units_long = pd.DataFrame(data=units_long, index=pair.equity1.data.index, columns=["Units Long"])
        units_long.fillna(method='ffill', inplace=True)

        units_short[0] = 0
        units_short[short_entry] = -1
        units_short[short_exit] = 0
        units_short = pd.DataFrame(data=units_short, index=pair.equity1.data.index, columns=["Units Short"])
        units_short.fillna(method='ffill', inplace=True)

        units = units_short.values + units_long.values

        # convert units into a n * 2 matrix (due to pair of equities)
        units = np.tile(units, [1, 2])

        # get hedges and format as a matrix of 1s and -h for share allocation
        hedge_ratio = pair.hedge_ols(lookback)
        share_allocation = ts.add_constant(-hedge_ratio)

        # get closed prices
        df = pd.concat([pair.equity1.closed, pair.equity2.closed], axis=1)

        # calculate capital allocation by element wise mult
        capital_allocation = share_allocation * df.values

        # calculate positions w/ bollinger units
        positions = units * capital_allocation

        # convert to df
        positions = pd.DataFrame(positions, index=pair.equity1.data.index)
        positions.columns = [pair.equity1.symbol, pair.equity2.symbol]

        # calculate profit and loss with % change of close price and positions
        close_pct_change = df.pct_change().values
        pnl = np.sum((positions.shift().values)*close_pct_change, axis=1)

        # calculate return
        total_position = np.sum(np.abs(positions.shift()), axis=1)
        ret = pnl / total_position

        # calculate cumulative return (add 1 for cumprod)
        cum_ret = pd.DataFrame((np.cumprod(1 + ret) - 1))
        cum_ret.fillna(method='ffill', inplace=True)

        self.cum_ret = cum_ret

    def plot_return(self):
        plt.plot(self.cum_ret)
        plt.show()

from helpers import equity
from helpers import pair

ibm = equity.Equity("GDX", "2020-01-01", "2021-01-01", "R25C111BKODO8RHT")
gld = equity.Equity("GLD", "2020-01-01", "2021-01-01", "R25C111BKODO8RHT")
port = pair.Pair(ibm, gld)
boll = BollingerPair(1,0,30,port)
boll.plot_return()

