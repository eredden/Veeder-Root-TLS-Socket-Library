import unittest
from src.tls_socket import tls_parser

# Verify that tls_parser() correctly parses bytecode output.
class test_tls_parser(unittest.TestCase):
    def test_example(self):
        command = "i10100"
        response = b'\x01i101002312301342020402&&FB3B\x03'
        expected_response = "2312301342020402&&FB3B"

        parsed_response = tls_parser(response, command)

        self.assertEqual(parsed_response, expected_response)
