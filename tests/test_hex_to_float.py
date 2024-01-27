import unittest
from src.tls_functions import hex_to_float

# Verify that hex_to_float() correctly makes IEEE floats out of hexadecimal codes.
class test_hex_to_float(unittest.TestCase):
    def test_hex_to_float(self):
        hex = "B8D1B717"
        test_response = hex_to_float(hex)
        expected_response = -0.0001

        self.assertEqual(test_response, expected_response)
