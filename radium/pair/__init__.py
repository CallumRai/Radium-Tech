from ._hedge_ols import *
from ._spread_ols import *
from .cadf_test import *
from .johansen_test import *


class Pair:
    def __init__(self, equity1, equity2):
        """
        Pair of equities (note: first equity is used as response variable in ols regression)
        Args:
            equity1: First equity in pair
            equity2: Second equity in pair
        """

        self.equity1 = equity1
        self.equity2 = equity2
        self.start_date = equity1.start_date
        self.end_date = equity1.end_date
