# test_socket.py - Tests whether or not the tlsSocket class operates as intended.

import unittest
import os
from datetime import date
from tls_socket import tlsSocket

class test_tlsSocket(unittest.TestCase):
    def test_tlsSocket(self):
        """
        Verify that tlsSocket.execute() and your system return the same date to test communication.
        """

        ip   = os.getenv("TLS_IP")
        port = os.getenv("TLS_PORT")

        with tlsSocket(ip, int(port)) as tls:
            today = date.today()
            expected = today.strftime("%y%m%d")
            actual = tls.execute("i10100")[:6]

        self.assertEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()