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
        Test correctness of Pair.budget method

        Visa price on 2021-01-01: 218.398245331 
        Mastercard price on 2021-01-01: 356.49165972
        """
        known_values = (([1.0, 1.0], 0, 574.88),
                        ([1.0, 1.0], 1, 5748.89),
                        ([1.0, 1.0], 2, 57488.99),
                        ([1.0, -1.0], 0, 574.88),
                        ([1.0, -1.0], 1, 5748.89),
                        ([1.0, -1.0], 2, 57488.99),
                        ([-1.0, 1.0], 0, 574.88),
                        ([-1.0, 1.0], 1, 5748.89),
                        ([-1.0, 1.0], 2, 57488.99),
                        ([1.0, 1.5555555], 0, 574.88),
                        ([1.0, 1.5555555], 1, 7531.35),
                        ([1.0, 1.5555555], 2, 77096.03),
                        ([1.0, 1.5555555], 3, 772742.77),
                        ([1.123456, 1.123456], 0, 574.88),
                        ([1.123456, 1.123456], 1, 6323.78),
                        ([1.123456, 1.123456], 2, 64387.66),
                        ([1.123456, 1.123456], 3, 645601.36))

        for hedge_ratio, decimals, budget in known_values:
            result = TestPair.V_MA.budget(hedge_ratio, decimals)
            self.assertEqual(budget, result)

    def test_budget_bad_input(self):
        """
        Test Exception handling of Pair.budget method
        """

        # Test bad decimal inputs
        self.assertRaises(TypeError, TestPair.V_MA.budget, [1.0, 1.5])
        self.assertRaises(TypeError, TestPair.V_MA.budget, [1.0, 1.5], 2.5)
        self.assertRaises(TypeError, TestPair.V_MA.budget, [1.0, 1.5], 'a')
        self.assertRaises(ValueError, TestPair.V_MA.budget, [1.0, 1.5], -3)

        # Test bad hedge_ratio inputs
        self.assertRaises(ValueError, TestPair.V_MA.budget, [], 1)
        self.assertRaises(ValueError, TestPair.V_MA.budget, [1], 1)
        self.assertRaises(ValueError, TestPair.V_MA.budget, [1,2,3], 1)
        self.assertRaises(TypeError, TestPair.V_MA.budget, ['1','2'], 1)
        self.assertRaises(TypeError, TestPair.V_MA.budget, 1, 1)



if __name__ == '__main__':
    unittest.main()

