# test_socket.py - Tests whether or not the TlsSocket class operates as intended.

import os
import unittest
from datetime import date
from veeder_root_tls_socket_library.socket import TlsSocket

class test_tlsSocket(unittest.TestCase):
    def setUp(self):
        self.ip   = os.getenv("TLS_IP")
        self.port = int(os.getenv("TLS_PORT"))

        if not self.ip or not self.port:
            raise ValueError("TLS_IP and TLS_PORT environment variables must have values.")
    
    def test_valid_command(self):
        """
        Verify that tlsSocket.execute() and your system return the same date to test communication.
        """

        today = date.today() 
        expected = today.strftime("%y%m%d")

        with TlsSocket(self.ip, self.port) as tls:
            actual = tls.execute("i10100")[:6]

        self.assertEqual(expected, actual)
    
    def test_invalid_command(self):
        """
        Verify that tlsSocket.execute() handles invalid commands by returning a ValueError.
        """

        with TlsSocket(self.ip, self.port) as tls:
            with self.assertRaises(ValueError):
                tls.execute("test")

if __name__ == "__main__":
    unittest.main()