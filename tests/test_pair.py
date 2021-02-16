import unittest
from radium import Pair, Equity


class TestPair(unittest.TestCase):
    API_KEY = ''
    with open('tests/api_key.txt') as file:
        API_KEY = file.readline()

    visa = Equity('V', '2015-01-01', '2021-01-01', API_KEY)
    mastercard = Equity('MA', '2015-01-01', '2021-01-01', API_KEY)
    v_ma = Pair(visa, mastercard)

    def test_default(self):
        """
        Returns: Conducts useless test to ensure setUp runs checks for no exceptions thrown

        """

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()

