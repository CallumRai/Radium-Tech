import math


def _truncate(number, decimals=0):
    """
    Truncates a number to a certain number of decimal places

    Parameters
    ----------
    number: numeric
        Number to truncate
    decimals: int
        Decimal places to truncate to, must be non-negative

    Returns
    -------
    ret: numeric
        Number truncated to specified decimal places

    Raises
    ------
    TypeError:
        Decimals is not an integer
    ValueError:
        Decimals is negative
    """

    if not isinstance(decimals, int):
        raise TypeError('Decimals must be an integer.')
    elif decimals < 0:
        raise ValueError('Decimals must be >= 0.')
    elif decimals == 0:
        # If decimals is zero can truncate as normal
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor
