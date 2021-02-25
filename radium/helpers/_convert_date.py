from datetime import date as datetime_date
from datetime import datetime


def _convert_date(date):
    """
    Converts a date to datetime.date type

    Parameters
    ----------
    date: str or datetime or datetime.date
        First date to plot in YYYY-MM-DD form

    Returns
    -------
    date: datetime.date
        date as datetime.date type

    Raises
    ------
    TypeError:
        Date not of types str or datetime or datetime.date
    """

    # Converts strings
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d").date()

    # Converts date object
    elif isinstance(date, datetime):
        date = date.date()

    # If not in required form input is incorrect
    if not isinstance(date, datetime_date):
        raise TypeError("date should be a string or datetime object")

    return date
