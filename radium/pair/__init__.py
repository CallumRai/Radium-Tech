from ._hedge_ols import _hedge_ols
from ._spread_ols import _spread_ols
from .cadf_test import CADF_Test
from .johansen_test import johansen_test
from ._budget import _budget


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
