# test_socket.py - Tests whether or not the TlsSocket class operates as intended.

from datetime import date
from os import environ
import unittest
from veeder_root_tls_socket_library.socket import TlsSocket

class test_tlsSocket(unittest.TestCase):
    def setUp(self):
        self.ip   = environ["TLS_IP"]
        self.port = int(environ["TLS_PORT"])

        if not self.ip or not self.port:
            raise ValueError("TLS_IP and TLS_PORT environment variables must have values.")
    
    def test_valid_command(self):
        """
        Verify that tlsSocket.execute() and your system return the same date to test communication.
        """

        today = date.today() 
        expected = today.strftime("%y%m")

        with TlsSocket(self.ip, self.port) as tls:
            actual = tls.execute("i10100")[:4]

        self.assertEqual(expected, actual)
    
    def test_invalid_command(self):
        """
        Verify that tlsSocket.execute() handles invalid commands by returning a ValueError.
        """

        with TlsSocket(self.ip, self.port) as tls:
            with self.assertRaises(ValueError):
                tls.execute("test")

    def test_checksum(self):
        """
        Verify that TlsSocket._data_integrity_check() correctly validates outputs.
        """

        # Cases are tuples with the full command output and expected checksum validation result.
        cases = [
            (b"\x01i101002312301342020402&&FB3B\x03", True),
            (b"\x01i101002312301342020402&&FB3A\x03", False),
            (b"\x01j101002312301342020402&&FB3B\x03", False)
        ]

        with TlsSocket(self.ip, self.port) as tls:
            for case in cases:
                actual = tls._data_integrity_check(case[0])
                expected = case[1]

                self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()