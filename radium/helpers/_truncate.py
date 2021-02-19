import math


def _truncate(number, decimals=0):
    """
    Truncates a number to a certain number of decimal places

    Args:
        number: Number to truncate
        decimals: Decimals to truncate to

    Returns: Number truncated to decimal place
    """

    if not isinstance(decimals, int):
        raise TypeError('Decimals must be an integer.')
    elif decimals < 0:
        raise ValueError('Decimals must be >= 0.')
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor
