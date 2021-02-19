import unittest

from radium import Pair, Equity
from radium.strategy import PairStrategy


class TestPairStrategy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open('tests/api_key.txt') as file:
            TestPairStrategy.API_KEY = file.readline()

        TestPairStrategy.visa = Equity('V', '2015-01-01', '2021-01-01',
                                        TestPairStrategy.API_KEY)
        TestPairStrategy.mastercard = Equity('MA', '2015-01-01', '2021-01-01',
                                              TestPairStrategy.API_KEY)
        TestPairStrategy.V_MA = Pair(TestPairStrategy.visa,
                                     TestPairStrategy.mastercard)
        TestPairStrategy.strategy = PairStrategy(TestPairStrategy.V_MA)

    def test_init_bad_input(self):
        """
        Test exception handling of PairStrategy.__init__ method
        """

        self.assertRaises(TypeError, PairStrategy, 'not pair')


if __name__ == '__main__':
    unittest.main()
