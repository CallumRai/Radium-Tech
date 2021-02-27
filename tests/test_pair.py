import unittest
from datetime import date
import numpy as np

from radium import Pair, Equity
from radium.pair import cadf_test, johansen_test
from radium.helpers import _truncate


class TestPair(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open('api_key.txt') as file:
            cls.API_KEY = file.readline()

        cls.visa = Equity('V', '2015-01-01', '2021-01-01', cls.API_KEY)
        cls.mastercard = Equity('MA', '2015-01-01', '2021-01-01', cls.API_KEY)
        cls.V_MA = Pair(cls.visa, cls.mastercard)

    def test_init_bad_input(self):
        """ 
        Test exception handling of Pair.__init__ method
        """

        self.assertRaises(TypeError, Pair, 'not equity', 'not equity')
        self.assertRaises(TypeError, Pair, TestPair.visa, 'not equity')
        self.assertRaises(TypeError, Pair, 'not equity', TestPair.visa)

        # Tests dates
        visa_bad = Equity('V', '2015-01-01', '2015-02-01', self.API_KEY)
        mastercard_bad = Equity('MA', '2016-01-01', '2016-02-01', self.API_KEY)
        with self.assertRaises(ValueError):
            Pair(visa_bad, mastercard_bad)

    def test_hedge_ratios_setter_good_input(self):
        """
        Test correctness of Pair.hedge_ratios setter method
        """

        TestPair.V_MA.hedge_ratios = ('OLS', 30)

        self.assertEqual(TestPair.V_MA.hedge_ratios.shape[1], 2)
        self.assertEqual(TestPair.V_MA.hedge_ratios[-2][0], 1)
        self.assertIsInstance(TestPair.V_MA.hedge_ratios[-2][1], np.float)
        self.assertTrue(TestPair.V_MA.hedge_ratios[-2][1] < 0)

    def test_hedge_ratios_setter_bad_input(self):
        """
        Test exception handling of hedge_ratios setter method
        """

        with self.assertRaises(TypeError):
            TestPair.V_MA.hedge_ratios = 'OLS'
        with self.assertRaises(TypeError):
            TestPair.V_MA.hedge_ratios = ['OLS', 30]
        with self.assertRaises(TypeError):
            TestPair.V_MA.hedge_ratios = ('OLS', 30, 1)
        with self.assertRaises(TypeError):
            TestPair.V_MA.hedge_ratios = (0, 30)
        with self.assertRaises(TypeError):
            TestPair.V_MA.hedge_ratios = ('OLS', 30.5)
        with self.assertRaises(ValueError):
            TestPair.V_MA.hedge_ratios = ('OLS', 0)
        with self.assertRaises(ValueError):
            TestPair.V_MA.hedge_ratios = ('OLS', -10)
        with self.assertRaises(ValueError):
            TestPair.V_MA.hedge_ratios = ('ols', 30)

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
            TestPair.V_MA._hedge_ratios = hedge_ratios
            self.assertEqual(spread,
                             _truncate(TestPair.V_MA.price_spread[-1], 2))
            del TestPair.V_MA._price_spread

    def test_price_spread_bad_input(self):
        """
        Test exception handling of Pair.price_spread
        """

        del TestPair.V_MA._hedge_ratios
        with self.assertRaises(Exception):
            TestPair.V_MA.price_spread

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
        self.assertRaises(ValueError, TestPair.V_MA.budget, [1, 2, 3], 1)
        self.assertRaises(TypeError, TestPair.V_MA.budget, ['1', '2'], 1)
        self.assertRaises(TypeError, TestPair.V_MA.budget, 1, 1)

    def test_plot_closed_bad_input(self):
        """
        Test exception handling of Pair.plot_closed methods.
        """

        # Wrong date ranges
        self.assertRaises(ValueError,
                          TestPair.V_MA.plot_closed,
                          '2016-01-01',
                          '2015-01-01')
        self.assertRaises(ValueError,
                          TestPair.V_MA.plot_closed,
                          date(2014, 1, 1))
        self.assertRaises(ValueError,
                          TestPair.V_MA.plot_closed,
                          date(2022, 1, 1))


# Test radium.pair functions outside Pair class
class TestPairFunctions(unittest.TestCase):

    def test_cadf_test_bad_input(self):
        """
        Test exception handling of cadf_test
        """

        self.assertRaises(TypeError, cadf_test, 'bad input')

    def test_johansen_test_bad_input(self):
        """
        Test exception handling of johansen_test
        """

        self.assertRaises(TypeError, johansen_test, 'bad input')


if __name__ == '__main__':
    unittest.main()
