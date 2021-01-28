import numpy as np

def calculate_returns(strategy):
    """
    Args:
        strategy: Strategy with positions

    Returns: Calculate returns acounting for budget and comissiopn

    """
    # Get the optimal positions determined by the strategy
    optimal_positions = strategy.get_optimal_positions()

    # Calculate integer positions determined by rounding optimal positions to 3 d.p.
    rounded_positions = np.zeros(optimal_positions.shape)
    for i in range(strategy.lookback, optimal_positions.shape[0] - 1):
        rounded_positions[i, 0] = budget.truncate(optimal_positions[i, 0], 3) * 10 ** 3
        rounded_positions[i, 1] = budget.truncate(optimal_positions[i, 1], 3) * 10 ** 3

    # Get closed prices
    prices = pd.concat([strategy.pair.equity1.closed, strategy.pair.equity2.closed], axis=1)
    prices.columns = [strategy.pair.equity1.symbol, strategy.pair.equity2.symbol]

    # Calculate orders
    equity1_orders = np.diff(rounded_positions[:, 0])
    equity1_orders = np.append(equity1_orders, 0)
    equity2_orders = np.diff(rounded_positions[:, 1])
    equity2_orders = np.append(equity2_orders, 0)

    # Calculate commissions per daily order (minimum price of 0.35)
    equity1_comm = np.array([max(abs(x) * 0.0035, 0.35) if x != 0 else 0 for x in equity1_orders])
    equity2_comm = np.array([max(abs(x) * 0.0035, 0.35) if x != 0 else 0 for x in equity2_orders])

    # Get balance
    equity1_balance = equity1_orders * prices.iloc[:, 0].values
    equity2_balance = equity2_orders * prices.iloc[:, 1].values