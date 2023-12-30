import socket
import time

class tlsSocket:
    """
    Defines a socket for the TLS-3XX and TLS-4XX systems manufactured by Veeder-Root.

    execute() - Used to send a command and view the output in accordance with Veeder-Root Serial Interface Manual 576013-635.
    """

    def __init__(self, ip: str, port: int):
        # Code to run when the class is created.
        self.ip = ip
        self.port = port

        # Sets up socket and attempts connection, throws exception if that fails.
        socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            socket_connection.connect((self.ip, self.port))
            self.socket = socket_connection
        
        except Exception as exception:
            raise exception
        
    def __str__(self):
        # Code to run to make the class more human-readable when printed.
        return f"tlsSocket({self.ip}, {self.port}, {self.socket})"

    def __enter__(self):
        # Code to run when entering a with statement.
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Code to run when exiting a with statement, including cleanup.
        socket = self.socket
        socket.close()

    def execute(self, command: bytes, timeout: int, display_format: bool) -> None:

        """
        Sends a command to a socket connection using the command format from the Veeder-Root Serial Interface Manual 576013-635.

        command - The function code you would like to execute. Make sure this is in computer format. \n
        timeout - The amount of time to wait for a response from the host. Adjust this as needed. \n
        display_format - Outputs values as strings instead of as bytecode.
        """

        socket = self.socket

        # Appends CTRL + A as the start of header.
        command = b"\x01" + command

        # Send input, wait, receive output.
        socket.sendall(command)
        time.sleep(timeout)
        response = socket.recv(512)

        # Error handling when an invalid command is used (9999FF1B).
        if b"FF1B" in response:
            response = b"Unrecognized function code. Use the command format form of the function."
            # Prevents the above error from getting first and last letters removed.
            display_format = False

        # Send output as string if display_format is enabled.
        if display_format: 
            response = response.decode("utf-8")
            
            # Removes SOH from being shown in output.
            response = response[1::]
            # Removes ETX from being shown in output.
            response = response[:-1]
            # Checks for newlines at end of output, removes if present.
            if response[-4:] == "\r\n\r\n":
                response = response[:-4]

        print(response)
