import numpy as np
import pandas as pd

from radium import Pair


class PairStrategy:
    """
    Base class for equity pair trading strategies.

    Attributes
    ----------
    daily_returns
    cum_returns
    CAGR 
    sharpe
    pair : radium.pair
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
    def daily_returns(self):
        """
        np.float[] : daily returns from trading by optimal positions

        Raises
        ------
        Exception
            If self.th_positions isn't defined
        """

        if hasattr(self, 'th_positions') == False:
            raise Exception('PairStrategy.th_positions is not defined')

        # Calculate th_daily_returns if undefined
        if hasattr(self, '_th_daily_returns') == False:
            # Get closed prices
            prices = pd.concat(
                [self.pair.equity1.closed, self.pair.equity2.closed], axis=1)

            # Calculate capital allocation to each position
            position_values = self.th_positions * prices.values

            # Convert positions_values to DataFrame
            position_values = pd.DataFrame(position_values,
                                           index=self.pair.equity1.data.index)
            position_values.columns = [self.pair.equity1.symbol,
                                       self.pair.equity2.symbol]

            # Calculate P&L with % change of close price and positions
            close_pct_change = prices.pct_change().values
            pnl = np.sum(position_values.shift().values * close_pct_change,
                         axis=1)

            # Calculate total position values the day before
            total_position_values = np.sum(np.abs(position_values.shift()),
                                           axis=1)
            self._th_daily_returns = pnl / total_position_values

        return self._th_daily_returns

    @property
    def cum_returns(self):
        """
        np.float[] : daily cumulative returns from trading by optimal positions.

        Raises
        ------
        Exception
            If self.th_positions is not defined
        """

        if hasattr(self, 'th_positions') == False:
            raise Exception('PairStrategy.th_positions is not defined')

        # Calculate cum_returns if undefined
        if hasattr(self, '_cum_returns') == False:
            # TODO: Determine 252vs365 days
            # ret = self.daily_returns
            # cum_ret = pd.DataFrame((np.cumprod(1 + ret) - 1))
            # cum_ret.fillna(method='ffill', inplace=True)
            # self._cum_returns = cum_ret.to_numpy()

            self._cum_returns = np.cumprod(1 + self.daily_returns) - 1

        return self._cum_returns

    @property
    def CAGR(self):
        """
        float: compound annual growth rate based upon daily cumulative returns.

        Raises
        ------
        Exception
            If self.th_positions is not defined.
        """

        if hasattr(self, 'th_positions') == False:
            raise Exception('PairStrategy.th_positions is not defined')

        # Calculate CAGR if undefined
        if hasattr(self, '_CAGR') == False:
            start_date = self.pair.start_date
            end_date = self.pair.end_date

            days = (end_date - start_date).days
            days = int(days)

            self._CAGR = (1 + self.cum_returns[-1]) ** (365 / days) - 1

        return self._CAGR

    @property
    def sharpe(self):
        """
        float: sharpe ratio of the strategy.

        Measures the performance of an investment compared to a risk-free asset,
        after adjusting for its risk.

        Exception
            If self.th_positions is not defined
        """

        if hasattr(self, 'th_positions') == False:
            raise Exception('PairStrategy.th_positions is not defined')

        if hasattr(self, '_sharpe') == False:
            ret = self.daily_returns
            self._sharpe = np.sqrt(252) * np.mean(ret) / np.std(ret)

        return self._sharpe

# TODO: Research how to calculate.
#    @property
#     def max_drawdown(self):
#        """
#        Calculates the maximum drawdown of the investment.
#
#        The maximum observed loss from a peak to a trough of a portfolio, before
#        a new peak is attained.
#
#        Returns
#        -------
#        ret : float
#            Maximum drawdown
#
#        Raises
#        ------
#        Exception
#            If self.th_positions is not defined
#        """
#
#        if hasattr(self, '_th_positions') == False:
#            raise Exception('PairStrategy.th_positions is not defined')
#
#        if hasattr(self, '_max_drawdown') == False:
#            cum_ret = self.cum_returns
#            max_drawdown = (np.min(cum_ret) - np.max(cum_ret)) / np.max(cum_ret)
#            self._max_drawdown = max_drawdown
#
#     def MDD_duration(self):
#        """
#        Calculates duration between maximum drawdown peaks in days
#
#        Returns
#        -------
#        ret : int
#            Maximum drawdown duration
#        """
#
#        ret = self.th_returns()
#        max_drawdown_days = np.abs(np.argmax(ret) - np.argmax(min))
#        return max_drawdown_days
