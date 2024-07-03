# test_format.py - Used to test the functionality of functions in src/tls_format.py.

import unittest
from tls_format import get_timestamp, split_data, hex_to_float

class test_format(unittest.TestCase):
    def test_get_timestamp(self):
        """
        Verify that get_timestamp() correctly extracts timestamps from command output.
        """

        outputs = ["240626210300",
                   "230525200300",
                   "220424190300"]
        
        expected = [{"year": 24, "month": 6, "day": 26, "hour": 21, "minute": 3},
                    {"year": 23, "month": 5, "day": 25, "hour": 20, "minute": 3},
                    {"year": 22, "month": 4, "day": 24, "hour": 19, "minute": 3}]

        for index in range(0, len(outputs)):
            actual = get_timestamp(outputs[index])
            self.assertEqual(actual, expected[index])

    def test_split_data(self):
        """
        Verify that split_data() correctly splits apart chunks of data.
        """

        data = ["abcdefabcdef", 
                "zyxwzyxw", 
                "ABCabcABC",
                "ABCabcABC"]
        
        length = [3, 4, 3, 10]

        expected = [["abc", "def", "abc", "def"], 
                    ["zyxw", "zyxw"], 
                    ["ABC", "abc", "ABC"],
                    ["ABCabcABC"]]

        for index in range(0, len(data)):
            actual = split_data(data[index], length[index])
            self.assertEqual(actual, expected[index])

    def test_hex_to_float(self):
        """
        Verify that hex_to_float() correctly makes IEEE floats from hexadecimal codes.
        """

        hex_codes = ["3F800000", "B8D1B717", "C2C7FAE1", "461C4000"]
        expected  = [       1.0,    -0.0001,     -99.99,    10000.0]

        for index in range(0, len(hex_codes)):
            actual = hex_to_float(hex_codes[index])
            self.assertEqual(actual, expected[index])

if __name__ == "__main__":
    unittest.main()