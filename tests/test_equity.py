import unittest
from radium.equity import *


class TestEquity(unittest.TestCase):
    def setUp(self):
        visa = Equity('V', '2015-01-01', '2021-01-01', 'A6O7S12U02K5YZO7')

    def test_default(self):
        """
        Returns: Conducts useless test to ensure setUp runs checks for no exceptions thrown

        """

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
