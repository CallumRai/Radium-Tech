from .johansen_test import *
import numpy as np
import math
from ..helpers.truncate import truncate

def budget(pair):
    """
    Args:
        pair: Pair of equities

    Returns: Budget to different decimal places

    """
    # Get the prices at end_date
    equity1_price = pair.equity1.closed.iloc[0]
    equity2_price = pair.equity2.closed.iloc[0]

    # Calculate theoretical ratios
    ratios_th = johansen_test(pair)

    # Calculate ratios to 4 decimal places, 3 d.p., ..., 1 d.p
    ratios_4dp = np.array([truncate(n, 4) for n in ratios_th])
    ratios_3dp = np.array([truncate(n, 3) for n in ratios_th])
    ratios_2dp = np.array([truncate(n, 2) for n in ratios_th])
    ratios_1dp = np.array([truncate(n, 1) for n in ratios_th])

    # Calculate budgets for 4 dp, 3 dp, ..., 1 dp
    budget_4dp = equity1_price * ratios_4dp[0] * 10000 + equity2_price * ratios_4dp[1] * 10000
    budget_3dp = equity1_price * ratios_3dp[0] * 1000 + equity2_price * ratios_3dp[1] * 1000
    budget_2dp = equity1_price * ratios_2dp[0] * 100 + equity2_price * ratios_2dp[1] * 100
    budget_1dp = equity1_price * ratios_1dp[0] * 10 + equity2_price * ratios_1dp[1] * 10

    print(f'Budget when rounding to 4 decimal places: ${math.trunc(budget_4dp)}')
    print(f'Budget when rounding to 3 decimal places: ${math.trunc(budget_3dp)}')
    print(f'Budget when rounding to 2 decimal places: ${math.trunc(budget_2dp)}')
    print(f'Budget when rounding to 1 decimal places: ${math.trunc(budget_1dp)}')
