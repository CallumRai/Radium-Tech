import numpy as np
import pandas as pd

from radium import Pair

class PairStrategy:
    """
    Base class for equity pair trading strategies.

    The positions and th_positions properties will be defined in the child class

    Attributes
    ----------
    th_positions
    th_daily_returns
    th_annualised_returns : float
        Theoretical geometric average amount of money earned by an investment
        each year over a given time period.
    th_sharpe_ratio : float
    th_max_drawdown : float
    th_max_drawdown_duration : int
        Number of days maximum drawdown lasted.
    """

    def __init__(self, pair):
        """
        Initialises PairStrategy class

        Parameters
        ----------
        pair : radium.Pair

        Raises
        ------
        TypeError
            If pair isn't radium.Pair.
        """
        # Exception handling
        if not isinstance(pair, Pair):
            raise TypeError('pair must be an radium.Pair object')
        self.pair = pair

    @property
    def th_positions(self):
        """
        np.float[][2] : Theoretical unrounded number of equities long/short each
                        day.

        Will be overridden in the child class.
        """
        return self._th_positions

    @property
    def th_daily_returns(self):
        """
        np.float[]: Theoretical daily returns without budget restrains/costs.

        Will be overridden in the child class.
        """
        return self._th_daily_returns

    def th_returns(self):
        """
        Calculates theoretical returns without accounting for budget and commission

        Returns: Theoretical returns as 2D array
        """

        # Get the optimal positions determined by the strategy
        optimal_positions = self.positions()

        # Get closed prices
        df = pd.concat([self.pair.equity1.closed, self.pair.equity2.closed], axis=1)

        # Calculate capital allocation to each position
        positions = optimal_positions * df.values

        # Convert to df
        positions = pd.DataFrame(positions, index=self.pair.equity1.data.index)
        positions.columns = [self.pair.equity1.symbol, self.pair.equity2.symbol]

        # Calculate profit and loss with % change of close price and positions
        close_pct_change = df.pct_change().values
        pnl = np.sum(positions.shift().values * close_pct_change, axis=1)

        # Calculate return
        total_position = np.sum(np.abs(positions.shift()), axis=1)
        ret = pnl / total_position

        return ret

    def cum_returns(self):
        """
        Returns: Cumulative returns as array

        """
        ret = self.th_returns()
        cum_ret = pd.DataFrame((np.cumprod(1 + ret) - 1))
        cum_ret.fillna(method='ffill', inplace=True)

        return cum_ret.values.flatten()

    def ann_returns(self):
        """
        Returns: Annualised returns

        """
        start_date = self.pair.start_date
        end_date = self.pair.end_date

        days = (end_date - start_date).days
        days = int(days)

        cum_returns = self.cum_returns()
        final_cum = cum_returns[-1]

        ann_return = (1 + final_cum) ** (365 / days) - 1
        return ann_return

    def sharpe(self):
        """
        Returns: Sharpe ratio

        """
        ret = self.th_returns()
        sharpe_ratio = np.sqrt(252) * np.mean(ret) / np.std(ret)
        return sharpe_ratio

    def MDD(self):
        """
        Returns: Maximum drawdown

        """
        ret = self.th_returns()
        max_drawdown = (np.min(ret) - np.max(ret)) / np.max(ret)
        return max_drawdown

    def MDD_duration(self):
        """
        Returns: Maximum drawdown duration in days

        """
        ret = self.th_returns()
        max_drawdown_days = np.abs(np.argmax(ret) - np.argmax(min))
        return max_drawdown_days
