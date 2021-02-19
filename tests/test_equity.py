import unittest
from radium import Equity


class TestEquity(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open('api_key.txt') as file:
            TestEquity.API_KEY = file.readline()

        TestEquity.visa = Equity('V', '2015-01-01', '2021-01-01', TestEquity.API_KEY)

    def test_init_bad_date(self):
        """
        Test error handling of end_date being before or some as start_date in defining equity class

        """
        with self.assertRaises(Exception):
            Equity('V', '2015-01-02', '2015-01-02', TestEquity.API_KEY)

        with self.assertRaises(Exception):
            Equity('V', '2015-01-02', '2015-01-01', TestEquity.API_KEY)

    def test_init_bad_symbol(self):
        """
        Test error handling of using an invalid symbol in defining equity class

        """
        with self.assertRaises(TypeError):
            Equity('asifhj', '2015-01-02', '2015-01-02', TestEquity.API_KEY)

    def test_plot_bad_date(self):
        """
        Test error handling of inval

        """
if __name__ == '__main__':
    unittest.main()
