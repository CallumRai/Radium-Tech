import unittest
from radium import Equity
from datetime import datetime


class TestEquity(unittest.TestCase):

    def setUp(self) -> None:
        with open('api_key.txt') as file:
            self.API_KEY = file.readline()

        self.visa = Equity('V', '2015-01-01', '2015-03-01', self.API_KEY)

    def test_init_bad_date(self):
        """
        Test error handling of end_date being before or some as start_date in defining equity class

        """

        with self.assertRaises(Exception):
            Equity('V', '2015-01-02', '2015-01-02', self.API_KEY)

        with self.assertRaises(Exception):
            Equity('V', '2015-01-02', '2015-01-01', self.API_KEY)

    def test_init_bad_symbol(self):
        """
        Test error handling of using an invalid symbol in defining equity class

        """

        with self.assertRaises(TypeError):
            Equity('asifhj', '2015-01-02', '2015-01-05', self.API_KEY)

    def test_plot_bad_date(self):
        """
        Test error handling of invalid date in plotting

        """

        with self.assertRaises(Exception):
            self.visa.plot('2015-01-02', '2015-01-02')

        with self.assertRaises(Exception):
            self.visa.plot('2015-01-02', '2015-01-01')

    def test_price_data(self):
        """
        Make sure right price data is used

        """

        # Known values for jan 2nd, feb 2nd 2015
        high = [266.75, 256.31]
        low = [262.49, 249.7]
        open = [263.38, 256.31]
        closed = [63.5205770973, 61.2004533847]

        jan_date = datetime.strptime("2015-01-02", "%Y-%m-%d").date()
        feb_date = datetime.strptime("2015-02-02", "%Y-%m-%d").date()

        dates = [jan_date, feb_date]

        for i in range(2):
            date = dates[i]

            self.assertEqual(high[i], self.visa.high[self.visa.high.index == date].item())
            self.assertEqual(low[i], self.visa.low[self.visa.low.index == date].item())
            self.assertEqual(open[i], self.visa.open[self.visa.open.index == date].item())
            self.assertEqual(closed[i], self.visa.closed[self.visa.closed.index == date].item())


if __name__ == '__main__':
    unittest.main()
