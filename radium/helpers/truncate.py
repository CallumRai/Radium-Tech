import math


def truncate(number, decimals=0):
    """
    Truncates a number to a certain number of decimal places

    Args:
        number: Number to truncate
        decimals: Decimals to truncate to

    Returns: Number truncated to decimal place
    """

    if not isinstance(decimals, int):
        raise TypeError('Decimal places must be an integer.')
    elif decimals < 0:
        raise ValueError('Decimal places has to be >= 0.')
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor
