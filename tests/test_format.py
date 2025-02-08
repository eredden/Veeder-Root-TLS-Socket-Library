# test_format.py - Used to test the functionality of functions in format.py.

import unittest
from veeder_root_tls_socket_library.format import _get_timestamp, _split_data, _hex_to_float

class test_format(unittest.TestCase):
    def test_get_timestamp(self):
        """
        Verify that get_timestamp() correctly extracts timestamps from command output.
        """
        # Cases are tuples with unformatted timestamps and formatted timestamps.
        cases = [
            ("240626210300", {"year": 24, "month": 6, "day": 26, "hour": 21, "minute": 3}),
            ("230525200300", {"year": 23, "month": 5, "day": 25, "hour": 20, "minute": 3}),
            ("220424190300", {"year": 22, "month": 4, "day": 24, "hour": 19, "minute": 3})
        ]

        for case in cases:
            actual = _get_timestamp(case[0])
            expected = case[1]

            self.assertEqual(actual, expected)


    def test_split_data(self):
        """
        Verify that split_data() correctly splits apart chunks of data.
        """

        inputs = [
            "abcdefabcdef", 
            "zyxwzyxw", 
            "ABCabcABC",
            "ABCabcABC"
        ]
        
        length = [3, 4, 3, 10]

        expected = [
            ["abc", "def", "abc", "def"], 
            ["zyxw", "zyxw"], 
            ["ABC", "abc", "ABC"],
            ["ABCabcABC"]
        ]

        for index in range(0, len(inputs)):
            actual = _split_data(inputs[index], length[index])
            self.assertEqual(actual, expected[index])

    def test_hex_to_float(self):
        """
        Verify that hex_to_float() correctly makes IEEE floats from hexadecimal codes.
        """

        # Cases are tuples with a hexadecimal float and the equivalent decimal float.
        cases = [
            ("3F800000",     1.0),
            ("B8D1B717", -0.0001),
            ("C2C7FAE1",  -99.99),
            ("461C4000", 10000.0)
        ]

        for case in cases:
            actual = _hex_to_float(case[0])
            expected = case[1]

            self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()