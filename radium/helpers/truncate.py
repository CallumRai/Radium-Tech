import math

def truncate(number, decimals = 0):
    """
    Args:
        number
        decimals

    Returns: Returns a value truncated to a specific number of decimal places

    """

    if not isinstance(decimals, int):
        raise TypeError('Decimal places must be an integer.')
    elif decimals < 0:
        raise ValueError('Decimal places has to be >= 0.')
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor