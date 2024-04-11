import unittest
from src.tls_3xx_functions import hex_to_float

# Verify that hex_to_float() correctly makes IEEE floats from hexadecimal codes.
class test_hex_to_float(unittest.TestCase):
    def test_hex_to_float(self):
        hex_codes = ["3F800000", "B8D1B717", "C2C7FAE1", "461C4000"]
        expected  = [       1.0,    -0.0001,     -99.99,    10000.0]

        for index in range(0, len(hex_codes)):
            actual = hex_to_float(hex_codes[index])
            self.assertEqual(actual, expected[index])

if __name__ == "__main__":
    unittest.main()