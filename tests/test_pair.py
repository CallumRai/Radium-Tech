import unittest
from radium import Pair, Equity


class TestPair(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open('tests/api_key.txt') as file:
            API_KEY = file.readline()

        visa = Equity('V', '2015-01-01', '2021-01-01', API_KEY)
        mastercard = Equity('MA', '2015-01-01', '2021-01-01', API_KEY)
        TestPair.V_MA = Pair(visa, mastercard)

    def test_budget_good_input(self):
        """
        Test correctness of budget method

        Visa price on 2021-01-01: 218.398245331 
        Mastercard price on 2021-01-01: 356.49165972
        """
        known_values = (([1,1], 0, 574.88),
                        ([1,1], 1, 5748.89),
                        ([1,1], 2, 57488.99),
                        ([1,-1], 0, 574.88),
                        ([1,-1], 1, 5748.89),
                        ([1,-1], 2, 57488.99),
                        ([-1,1], 0, 574.88),
                        ([-1,1], 1, 5748.89),
                        ([-1,1], 2, 57488.99),
                        ([1, 1.5555555], 0, 574.88),
                        ([1, 1.5555555], 1, 7531.35),
                        ([1, 1.5555555], 2, 77096.03),
                        ([1, 1.5555555], 3, 772742.77),
                        ([1.123456, 1.123456], 0, 574.88),
                        ([1.123456, 1.123456], 1, 6323.78),
                        ([1.123456, 1.123456], 2, 64387.66),
                        ([1.123456, 1.123456], 3, 645601.36))

        for hedge_ratio, decimals, budget in known_values:
            result = TestPair.V_MA.budget(hedge_ratio, decimals)
            self.assertEqual(budget, result)


if __name__ == '__main__':
    unittest.main()

