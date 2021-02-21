import numpy as np
import pandas as pd

from radium import Pair

class PairStrategy:
    """
    Base class for equity pair trading strategies.

    The th_positions properties will be defined in the child class.

    Attributes
    ----------
    th_positions
    th_daily_returns
    cum_returns
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
    def daily_returns(self):
        self._daily_returns = self.th_daily_returns

        return self._daily_returns

    @property
    def th_daily_returns(self):
        """
        np.float[]: ndarray of daily returns 

        Calculates theoretical daily returns without budget restrains/costs.

        Raises
        ------
        Exception
            If self.th_positions isn't defined
        """

        if hasattr(self, '_th_positions') == False:
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
        np.float[]: ndarray of cumulative returns of the strategy

        Calculates daily cumulative returns 

        Raises
        ------
        Exception
            If self.th_positions is not defined
        """
        
        # Calculate th_cum_returns if undefined
        if hasattr(self, '_cum_returns') == False:
            #TODO: Determine 252vs365 days
            #ret = self.daily_returns
            #cum_ret = pd.DataFrame((np.cumprod(1 + ret) - 1))
            #cum_ret.fillna(method='ffill', inplace=True)
            #self._cum_returns = cum_ret.to_numpy()

            self._cum_returns = np.cumprod(1 + self.daily_returns) - 1

        return self._cum_returns

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
        ret = self.th_daily_returns
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
