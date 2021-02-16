import unittest
from radium.equity import Equity
from radium.pair import Pair
from radium.strategy import BollingerPair


class TestBollingerPair(unittest.TestCase):
    def setUp(self):
        visa = Equity('V', '2015-01-01', '2021-01-01', API_KEY)
        mastercard = Equity('MA', '2015-01-01', '2021-01-01', API_KEY)
        v_ma = Pair(visa, mastercard)
        v_ma_boll = BollingerPair(v_ma, 1, 0, 20)
        v_ma_boll.plot()

    def test_default(self):
        """
        Returns: Conducts useless test to ensure setUp runs checks for no exceptions thrown

        """

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
