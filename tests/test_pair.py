import unittest
from datetime import date
import numpy as np

from radium import Pair, Equity
from radium.pair import cadf_test
from radium.helpers import _truncate


class TestPair(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open('tests/api_key.txt') as file:
            TestPair.API_KEY = file.readline()

        TestPair.visa = \
                Equity('V', '2015-01-01', '2021-01-01', TestPair.API_KEY)
        TestPair.mastercard = \
                Equity('MA', '2015-01-01', '2021-01-01', TestPair.API_KEY)
        TestPair.V_MA = Pair(TestPair.visa, TestPair.mastercard)

    def test_init_bad_input(self):
        """ 
        Test exception handling of Pair.__init__ method
        """

        self.assertRaises(TypeError, Pair, 'not equity', 'not equity')
        self.assertRaises(TypeError, Pair, TestPair.visa, 'not equity')
        self.assertRaises(TypeError, Pair, 'not equity', TestPair.visa)

    def test_hedge_ols_good_input(self):
        """
        Test correctnes of Pair.hedge_ols method
        """

        hedge_ratios = TestPair.V_MA.hedge_ols(30)

        self.assertEqual(hedge_ratios.shape[1], 2)
        self.assertEqual(hedge_ratios[-2][0], 1)
        self.assertIsInstance(hedge_ratios[-2][1], np.float)
        self.assertTrue(hedge_ratios[-2][1] < 0)


    def test_hedge_ols_bad_input(self):
        """
        Test exception handling of Pair.hedge_ols
        """

        self.assertRaises(TypeError, TestPair.V_MA.hedge_ols, 'a')
        self.assertRaises(TypeError, TestPair.V_MA.hedge_ols, 1.5)
        self.assertRaises(ValueError, TestPair.V_MA.hedge_ols, 0)
        self.assertRaises(ValueError, TestPair.V_MA.hedge_ols, -10)

    def test_price_spread_good_input(self):
        """
        Test correctness of Pair.price_spread
        """
        shape0 = TestPair.visa.closed.shape[0]
        hedge_ratios1 = np.ones((shape0, 2))
        hedge_ratios2 = np.full((shape0, 2), 2)
        hedge_ratios3 = np.full((shape0, 2), 1.5)

        hedge_ratios4 = np.ones((shape0, 2))
        hedge_ratios4[:, 1] *= -1
        hedge_ratios5 = np.full((shape0, 2), 2)
        hedge_ratios5[:, 1] *= -1
        hedge_ratios6 = np.full((shape0, 2), 1.5)
        hedge_ratios6[:, 1] *= -1

        known_values = ((hedge_ratios1, 574.88),
                        (hedge_ratios2, 1149.77),
                        (hedge_ratios3, 862.33),
                        (hedge_ratios4, -138.09),
                        (hedge_ratios5, -276.18),
                        (hedge_ratios6, -207.14))

        for hedge_ratios, spread in known_values:
            result = TestPair.V_MA.price_spread(hedge_ratios)
            truncated_last_result = _truncate(result[0], 2)
            self.assertEqual(spread, truncated_last_result)

    def test_price_spread_bad_input(self):
        """
        Test excpetion handling of Pair.hedge_ols
        """

        self.assertRaises(TypeError, TestPair.V_MA.price_spread, [])
        self.assertRaises(TypeError, TestPair.V_MA.price_spread, [[1, -0.5]])

        # Raise TypeError when hedge_ratios.shape[0] != equity1.closed.shape[0]
        self.assertRaises(TypeError,
                          TestPair.V_MA.price_spread,
                          np.ones((10, 2)))

        # Raise TypeError when hedge_ratios.shape[1] != 2
        shape0 = TestPair.visa.closed.shape[0]
        self.assertRaises(TypeError,
                          TestPair.V_MA.price_spread,
                          np.ones((shape0, 1)))
        self.assertRaises(TypeError,
                          TestPair.V_MA.price_spread,
                          np.ones((shape0, 3)))

    def test_budget_good_input(self):
        """
        Test correctness of Pair.budget method

        Visa price on 2020-12-31: 218.398245331 
        Mastercard price on 2020-12-311: 356.49165972
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
        Test exception handling of Pair.budget method.
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

    def test_plot_closed_bad_input(self):
        """
        Test exception handling of Pair.plot_closed methods.
        """

        # Wrong string formatting
        self.assertRaises(TypeError, TestPair.V_MA.plot_closed, '20150101')
        self.assertRaises(TypeError, TestPair.V_MA.plot_closed, '2015-20-01')
        self.assertRaises(TypeError,
                          TestPair.V_MA.plot_closed,
                          end_date='20180101')
        self.assertRaises(TypeError,
                          TestPair.V_MA.plot_closed,
                          end_date='2018-20-01')

        # Wrong input type
        self.assertRaises(TypeError, TestPair.V_MA.plot_closed, 20150101)
        self.assertRaises(TypeError, TestPair.V_MA.plot_closed, end_date=2015)

        # Wrong date ranges
        self.assertRaises(ValueError,
                          TestPair.V_MA.plot_closed,
                          '2016-01-01',
                          '2015-01-01')
        self.assertRaises(ValueError,
                          TestPair.V_MA.plot_closed,
                          date(2014,1,1))
        self.assertRaises(ValueError,
                          TestPair.V_MA.plot_closed,
                          date(2022,1,1))


# Test radium.pair functions outside Pair class
class TestPairFunctions(unittest.TestCase):

    def test_cadf_test_bad_input(self):
        """
        Test exception handling of cadf_test
        """

        self.assertRaises(TypeError, cadf_test, 'bad input')


if __name__ == '__main__':
    unittest.main()

