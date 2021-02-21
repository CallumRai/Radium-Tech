import unittest

from radium import Pair, Equity
from radium.strategy import PairStrategy


class TestPairStrategy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open('api_key.txt') as file:
            cls.API_KEY = file.readline()

        cls.visa = Equity('V', '2015-01-01', '2021-01-01', cls.API_KEY)
        cls.mastercard = Equity('MA', '2015-01-01', '2021-01-01', cls.API_KEY)
        cls.V_MA = Pair(cls.visa, cls.mastercard)
        cls.strategy = PairStrategy(cls.V_MA)

    def test_init_bad_input(self):
        """
        Test exception handling of PairStrategy.__init__ method
        """

        self.assertRaises(TypeError, PairStrategy, 'not pair')

    def test_th_daily_returns_bad_input(self):
        """
        Test exception handling of PairStrategy.th_daily_returns property
        """

        with self.assertRaises(Exception):
            TestPairStrategy.strategy.th_daily_returns

    def test_cum_returns_bad_input(self):
        """
        Test exception handling of PairStrategy.cum_returns property 
        """

        with self.assertRaises(Exception):
            TestPairStrategy.strategy.cum_returns

    def test_CAGR_bad_input(self):
        """
        Test excpetion handling of PairStrategy.CAGR property
        """

        with self.assertRaises(Exception):
            TestPairStrategy.strategy.CAGR


if __name__ == '__main__':
    unittest.main()
