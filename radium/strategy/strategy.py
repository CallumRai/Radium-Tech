import numpy as np
from radium.helpers import *
import pandas as pd


class Strategy:
    def __init__(self, pair):
        """
        Args:
            pair: Pair to run strategies on
        """

        self.pair = pair

    def returns(self):
        """
        Returns: Calculate returns acounting for budget and comissiopn

        """
        # Get the optimal positions determined by the strategy
        optimal_positions = self.positions()

        # Calculate integer positions determined by rounding optimal positions to 3 d.p.
        rounded_positions = np.zeros(optimal_positions.shape)
        for i in range(self.lookback, optimal_positions.shape[0] - 1):
            rounded_positions[i, 0] = truncate(optimal_positions[i, 0], 3) * 10 ** 3
            rounded_positions[i, 1] = truncate(optimal_positions[i, 1], 3) * 10 ** 3

        # Get closed prices
        prices = pd.concat([self.pair.equity1.closed, self.pair.equity2.closed], axis=1)

        # Calculate orders
        equity1_orders = np.diff(rounded_positions[:, 0])
        equity1_orders = np.append(0, equity1_orders)
        equity2_orders = np.diff(rounded_positions[:, 1])
        equity2_orders = np.append(0, equity2_orders)

        # Calculate commissions per daily order (minimum price of 0.35)
        equity1_comm = np.array([max(abs(x) * 0.0035, 0.35) if x != 0 else 0 for x in equity1_orders])
        equity2_comm = np.array([max(abs(x) * 0.0035, 0.35) if x != 0 else 0 for x in equity2_orders])

        # Calculate Initial Budget, equal to buy 1000 units of each equity
        init_budget = 1000 * (self.pair.equity1.closed.iloc[0] + self.pair.equity2.closed.iloc[0])
        # Truncate to 2 d.p.
        budget = truncate(init_budget, 2)

        # Calculate returns from Equity 1 and Equity 2
        for i in range(0, len(equity1_orders) - 1):
            budget += -1 * equity1_orders[i] * self.pair.equity1.closed.iloc[i] - equity1_comm[i]
            budget += -1 * equity2_orders[i] * self.pair.equity2.closed.iloc[i] - equity2_comm[i]

        return budget / init_budget - 1

    def th_returns(self):
        """
        Returns: theoretical returns without any costs and budget restrictions

        """

        # Get the optimal positions determined by the strategy
        optimal_positions = self.positions()

        # get closed prices
        df = pd.concat([self.pair.equity1.closed, self.pair.equity2.closed], axis=1)

        # calculate capital allocation to each position
        positions = optimal_positions * df.values

        # convert to df
        positions = pd.DataFrame(positions, index=self.pair.equity1.data.index)
        positions.columns = [self.pair.equity1.symbol, self.pair.equity2.symbol]

        # calculate profit and loss with % change of close price and positions
        close_pct_change = df.pct_change().values
        pnl = np.sum((positions.shift().values) * close_pct_change, axis=1)

        # calculate return
        total_position = np.sum(np.abs(positions.shift()), axis=1)
        ret = pnl / total_position

        return ret

    def cum_returns(self):
        """
        Returns: Cumulative Returns

        """
        ret = self.th_returns()

        # calculate cumulative return (add 1 for cumprod)
        cum_ret = pd.DataFrame((np.cumprod(1 + ret) - 1))
        cum_ret.fillna(method='ffill', inplace=True)

        return cum_ret

    def sharpe_ratio(self):
        """
        Returns: Sharpe ratio

        """
        ret = self.th_returns()

        sharpe_ratio = np.sqrt(252)*np.mean(ret)/np.std(ret)

        return sharpe_ratio