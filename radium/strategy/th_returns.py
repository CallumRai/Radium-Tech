import numpy as np
import pandas as pd


def th_returns(strategy):
    """
    Calculate theoretical returns without any costs and budget restrictions
    Store Cumulative Returns in strategy.cum_ret
    """
    # Get the optimal positions determined by the strategy
    optimal_positions = strategy.get_optimal_positions()

    # get closed prices
    df = pd.concat([strategy.pair.equity1.closed, strategy.pair.equity2.closed], axis=1)

    # calculate capital allocation to each position
    positions = optimal_positions * df.values

    # convert to df
    positions = pd.DataFrame(positions, index=strategy.pair.equity1.data.index)
    positions.columns = [strategy.pair.equity1.symbol, strategy.pair.equity2.symbol]

    # calculate profit and loss with % change of close price and positions
    close_pct_change = df.pct_change().values
    pnl = np.sum((positions.shift().values) * close_pct_change, axis=1)

    # calculate return
    total_position = np.sum(np.abs(positions.shift()), axis=1)
    ret = pnl / total_position

    # calculate cumulative return (add 1 for cumprod)
    cum_ret = pd.DataFrame((np.cumprod(1 + ret) - 1))
    cum_ret.fillna(method='ffill', inplace=True)

    strategy.cum_ret = cum_ret
    print(
        'APR = %f Sharpe = %f' % (np.prod(1 + ret) ** (252 / len(ret)) - 1, np.sqrt(252) * np.mean(ret) / np.std(ret)))
