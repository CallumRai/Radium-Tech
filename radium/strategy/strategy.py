import numpy as np
import pandas as pd
from radium.helpers import _truncate

class Strategy:
    def __init__(self, pair):
        """
        Base class for trading strategies upon pairs.

        Args:
            pair: Pair of equities to backtest strategy on

        """

        self.pair = pair

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
