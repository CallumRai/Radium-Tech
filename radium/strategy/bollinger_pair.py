from .pair_strategy import PairStrategy
import numpy as np
import statsmodels.tsa.stattools as ts
import pandas as pd


class BollingerPair(PairStrategy):
    """
    Bollinger band strategy on a pair of equities

    Attributes
    ----------
    pair: radium.Pair
    entry_z : float
        Z-score to enter position at
    exit_z: float
        Z-score to exit position at
    lookback: int
        Days looked back at on when calculating optimal positions
    th_positions : np.float[][2]
        Theoretical optimum positions calculated by strategy

    See Also
    --------
    radium.PairStrategy : Parent class
    """

    def __init__(self, pair, entry_z, exit_z, lookback):
        """
        Initialises strategy
        Parameters
        ----------
        pair: radium.Pair
        entry_z : float
            Z-score to enter position at
        exit_z : float
            Z-score to exit position at
        lookback : int
            Days to lookback on when calculating optimal positions
        """

        super().__init__(pair)

        self.entry_z = entry_z
        self.exit_z = exit_z
        self.lookback = lookback
        self.th_positions = self.calculate_positions()

    def calculate_positions(self):
        """
        Calculates theoretical optimum positions calculated by strategy

        Returns
        -------
        th_positions : np.float[][2]
        """

        spread = self.pair.price_spread

        # Calculate Z-score
        spread_mean = spread.rolling(self.lookback).mean()
        spread_std = spread.rolling(self.lookback).std()
        spread_z = (spread - spread_mean) / spread_std

        # Calculate long and short entry and exit points
        long_entry = spread_z < -self.entry_z
        long_exit = spread_z > -self.exit_z

        short_entry = spread_z > self.entry_z
        short_exit = spread_z < self.exit_z

        # Calculate number of units at each point
        units_long = np.zeros(long_entry.shape)
        units_long[:] = np.nan

        units_short = np.zeros(short_entry.shape)
        units_short[:] = np.nan

        units_long[0] = 0
        units_long[long_entry] = 1
        units_long[long_exit] = 0
        units_long = pd.DataFrame(data=units_long,
                                  index=self.pair.equity1.data.index,
                                  columns=["Units Long"])
        units_long.fillna(method='ffill', inplace=True)

        units_short[0] = 0
        units_short[short_entry] = -1
        units_short[short_exit] = 0
        units_short = pd.DataFrame(data=units_short,
                                   index=self.pair.equity1.data.index,
                                   columns=["Units Short"])
        units_short.fillna(method='ffill', inplace=True)

        units = units_short.values + units_long.values

        # Convert units into a n * 2 matrix (due to pair of equities)
        units = np.tile(units, [1, 2])

        # Optimal share positions determined by the Bollinger Bands strategy
        return units * self.pair.hedge_ratios
