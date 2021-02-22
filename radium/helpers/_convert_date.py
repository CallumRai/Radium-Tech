from datetime import date as datetime_date
from datetime import datetime


def _convert_date(date):
    """
    Converts a date to a datetime date if not already
    Parameters
    ----------
    date: Date as a "YYYY-MM-DD" string, datetime object or datetime date

    Returns
    -------
    Date as a datetime date
    """

    # Converts strings
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d").date()

    # Converts date object
    elif isinstance(date, datetime):
        date = date.date()

    # If not in required form input is incorrect
    if not isinstance(date, datetime_date):
        raise TypeError("Date should be a string or datetime object")

    return date
