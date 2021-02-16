import unittest
from src.helpers import _truncate

class TestTruncate(unittest.TestCase):
    def test_truncate_good_input(self):
        '''
        Test correctness of _truncate 
        '''
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
        '''
        _truncate should fail when decimals not integer
        '''
        self.assertRaises(TypeError, _truncate, 1.5, 'a')
        self.assertRaises(TypeError, _truncate, 1.5, 1.5)
        
    def test_negative(self):
        '''
        _truncate should fail when decimals negative
        '''
        self.assertRaises(ValueError, _truncate, 11, -1)
        self.assertRaises(ValueError, _truncate, -10, -2)


if __name__ == '__main__':
    unittest.main()
