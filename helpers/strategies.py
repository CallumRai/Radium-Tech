import numpy as np
import pandas as pd
import statsmodels.tsa.stattools as ts
import matplotlib.pyplot as plt
from budget import truncate

class BollingerPair():
    def __init__(self, pair, lookback, entry_z, exit_z):
        """
        :param entry_z: Entry Z-score
        :param exit_z: Exit Z-score
        :param lookback: Period to calculate Z-score over
        :param pair: Pair of interest
        """

        self.pair = pair
        self.lookback = lookback
        self.entry_z = entry_z
        self.exit_z = exit_z

    def get_optimal_positions(self):
        """
        Calculate the optimal share positions determined by the Bollinger Bands strategy
        -- returns: optimal_positions (WRITE THE STRUCTURE OF RETURN OBJECT)
        """

        # Get pair spread using ols estimate of hedge ratio w/ lookback
        spread = self.pair.spread_ols(self.lookback)

        # Calculate Z-score
        spread_mean = spread.rolling(self.lookback).mean()
        spread_std = spread.rolling(self.lookback).std()
        spread_z = (spread - spread_mean) / spread_std

        # Calculate long and short entry and exit points
        long_entry = spread_z < -self.entry_z
        long_exit = spread_z > -self.entry_z

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
        units_long = pd.DataFrame(data=units_long, index=self.pair.equity1.data.index, columns=["Units Long"])
        units_long.fillna(method='ffill', inplace=True)

        units_short[0] = 0
        units_short[short_entry] = -1
        units_short[short_exit] = 0
        units_short = pd.DataFrame(data=units_short, index=self.pair.equity1.data.index, columns=["Units Short"])
        units_short.fillna(method='ffill', inplace=True)

        units = units_short.values + units_long.values

        # convert units into a n * 2 matrix (due to pair of equities)
        units = np.tile(units, [1, 2])

        # get hedges and format as a matrix of 1s and -h for share allocation
        hedge_ratio = self.pair.hedge_ols(self.lookback)
        share_allocation = ts.add_constant(-hedge_ratio)

        # optimal positions detrmined by Bollinger Bands strategy
        optimal_positions = units * share_allocation

        return optimal_positions

    def theoretical_returns(self):
        """
        Calculate theoretical returns without any costs and budget restrictions
        Store Cumulative Returns in self.cum_ret
        """
        # Get the optimal positions determined by the strategy
        optimal_positions = self.get_optimal_positions()

        # get closed prices
        df = pd.concat([self.pair.equity1.closed, self.pair.equity2.closed], axis=1)

        # calculate capital allocation to each position
        positions = optimal_positions * df.values

        # convert to df
        positions = pd.DataFrame(positions, index=self.pair.equity1.data.index)
        positions.columns = [self.pair.equity1.symbol, self.pair.equity2.symbol]

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
        print('APR = %f Sharpe = %f' % (np.prod(1+ret)**(252/len(ret))-1, np.sqrt(252)*np.mean(ret)/np.std(ret)))

    def calculate_returns(self):
        """
        -- Calculate returns taking into account commision fees and budget restrictions
        -- Optimal Positions get rounded to 3 decimal places
        -- Store Cumulative Returns in self.cum_ret
        """
        # Get the optimal positions determined by the strategy
        optimal_positions = self.get_optimal_positions()

        # Calculate integer positions determined by rounding optimal positions to 3 d.p.
        rounded_positions = np.zeros(optimal_positions.shape)
        for i in range(self.lookback, optimal_positions.shape[0] - 1):
            rounded_positions[i, 0] = truncate(optimal_positions[i, 0], 3) * 10**3
            rounded_positions[i, 1] = truncate(optimal_positions[i, 1], 3) * 10**3

        # Get closed prices
        prices = pd.concat([self.pair.equity1.closed, self.pair.equity2.closed], axis=1)

        # Calculate orders
        equity1_orders = np.diff(rounded_positions[:, 0])
        equity1_orders = np.append(0, equity1_orders)
        equity2_orders = np.diff(rounded_positions[:, 1])
        equity2_orders = np.append(0, equity2_orders)

        # Calculate commissions per daily order (minimum price of 0.35)
        equity1_comm = np.array([max(abs(x)*0.0035, 0.35) if x != 0 else 0 for x in equity1_orders])
        equity2_comm = np.array([max(abs(x)*0.0035, 0.35) if x != 0 else 0 for x in equity2_orders])


        # Calculate Initial Budget, equal to buy 1000 units of each equity
        init_budget = 1000 * (self.pair.equity1.closed.iloc[0] + self.pair.equity2.closed.iloc[0])
        # Truncate to 2 d.p.
        budget = truncate(init_budget, 2)

        # Calculate returns from Equity 1 and Equity 2
        for i in range(0, len(equity1_orders) - 1):
            budget += -1 * equity1_orders[i] * self.pair.equity1.closed.iloc[i] - equity1_comm[i]
            budget += -1 * equity2_orders[i] * self.pair.equity2.closed.iloc[i] - equity2_comm[i]

        print(budget/init_budget - 1)




    def plot_return(self):
        plt.plot(self.cum_ret)
        plt.show()

if __name__ == '__main__':
    import equity
    import pair

    GDX = equity.Equity("GDX", "2020-01-01", "2021-01-01", "A6O7S12U02K5YZO7")
    GLD = equity.Equity("GLD", "2020-01-01", "2021-01-01", "A6O7S12U02K5YZO7")
    port = pair.Pair(GDX, GLD)
    boll = BollingerPair(port, 30, 1, 0)
    boll.calculate_returns()
#    boll.theoretical_returns()
#    boll.plot_return()
