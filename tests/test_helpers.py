import unittest
from radium.helpers import _truncate, _convert_date
from datetime import datetime


class TestTruncate(unittest.TestCase):
    def test_truncate_good_input(self):
        """
        Test correctness of _truncate
        """

        known_values = ((1.9999999, 0, 1.0),
                        (1.9999999, 1, 1.9),
                        (1.9999999, 2, 1.99),
                        (1.9999999, 3, 1.999),
                        (1.9999999, 4, 1.9999),
                        (1.9999999, 5, 1.99999),
                        (1.0, 0, 1.0),
                        (1.0, 1, 1.0),
                        (1.0, 2, 1.0),
                        (1.0, 3, 1.0))

        for number, decimals, truncated_number in known_values:
            result = _truncate(number, decimals)
            self.assertEqual(truncated_number, result)

    def test_not_integer(self):
        """
        _truncate should fail when decimals not integer
        """

        self.assertRaises(TypeError, _truncate, 1.5, 'a')
        self.assertRaises(TypeError, _truncate, 1.5, 1.5)

    def test_negative(self):
        """
        _truncate should fail when decimals negative
        """

        self.assertRaises(ValueError, _truncate, 11, -1)
        self.assertRaises(ValueError, _truncate, -10, -2)


class TestDate(unittest.TestCase):
    def setUp(self) -> None:
        self.date_str = "2020-01-01"
        self.datetime = datetime.strptime(self.date_str, "%Y-%m-%d")
        self.date = self.datetime.date()

    def test_str(self):
        """
        Tests function with a string input

        """

        self.assertEqual(self.date, _convert_date(self.date_str))

    def test_datetime(self):
        """
        Tests function with a datetime input

        """
        self.assertEqual(self.date, _convert_date(self.datetime))

    def test_date(self):
        """
        Tests function with a date input

        """
        self.assertEqual(self.date, _convert_date(self.date))

    def test_bad_str(self):
        """
        Tests function with a incorrect string input

        """
        with self.assertRaises(ValueError):
            _convert_date("sdkifsd")
        with self.assertRaises(ValueError):
            _convert_date("")

    def test_bad_type(self):
        """
        Tests function with a incorrect type as date

        """
        with self.assertRaises(TypeError):
            _convert_date(34)
        with self.assertRaises(TypeError):
            _convert_date([self.date])


if __name__ == '__main__':
    unittest.main()
