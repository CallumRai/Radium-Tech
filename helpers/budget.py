import math
import numpy as np
from tests import johansen_test
from data import adjusted_closed

def truncate(number, decimals = 0):
    '''
    Returns a value truncated to a specific number of decimal places
    '''
    if not isinstance(decimals, int):
        raise TypeError('Decimal places must be an integer.')
    elif decimals < 0:
        raise ValueError('Decimal places has to be >= 0.')
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor

def budget(symbol1, symbol2, start_date, end_date, key):

    # Get the prices at end_date
    symbol1_price = adjusted_closed(symbol1, start_date, end_date, key)['5. adjusted close'].iloc[0]
    symbol2_price = adjusted_closed(symbol2, start_date, end_date, key)['5. adjusted close'].iloc[0]

    # Calculate theoretical ratios
    ratios_th = johansen_test(symbol1, symbol2, start_date, end_date, key)

    # Calculate ratios to 4 decimal places, 3 d.p., ..., 1 d.p
    ratios_4dp = np.array([truncate(n, 4) for n in ratios_th])
    ratios_3dp = np.array([truncate(n, 3) for n in ratios_th])
    ratios_2dp = np.array([truncate(n, 2) for n in ratios_th])
    ratios_1dp = np.array([truncate(n, 1) for n in ratios_th])

    # Calculate budgets for 4 dp, 3 dp, ..., 1 dp
    budget_4dp = symbol1_price * ratios_4dp[0] * 10000 + symbol2_price * ratios_4dp[1] * 10000
    budget_3dp = symbol1_price * ratios_3dp[0] * 1000 + symbol2_price * ratios_3dp[1] * 1000
    budget_2dp = symbol1_price * ratios_2dp[0] * 100 + symbol2_price * ratios_2dp[1] * 100
    budget_1dp = symbol1_price * ratios_1dp[0] * 10 + symbol2_price * ratios_1dp[1] * 10

    print(f'Budget when rounding to 4 decimal places: ${math.trunc(budget_4dp)}')
    print(f'Budget when rounding to 3 decimal places: ${math.trunc(budget_3dp)}')
    print(f'Budget when rounding to 2 decimal places: ${math.trunc(budget_2dp)}')
    print(f'Budget when rounding to 1 decimal places: ${math.trunc(budget_1dp)}')

if __name__ == '__main__':
    budget("GLD", "GDX", '2019-01-01', '2021-01-01', "A6O7S12U02K5YZO7")
