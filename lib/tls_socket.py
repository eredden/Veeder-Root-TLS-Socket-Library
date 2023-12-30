import socket, time

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
    
    def __del__(self):
        # Code to run when deleting this class.
        socket = self.socket
        socket.close()

    def __enter__(self):
        # Code to run when entering a with statement.
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Code to run when exiting a with statement, including cleanup.
        socket = self.socket
        socket.close()

    def execute(self, command: bytes, timeout: int) -> None:

        """
        Sends a command to a socket connection using the command format from the Veeder-Root Serial Interface Manual 576013-635.
        """

        socket = self.socket

        # Appends CTRL + A as the start of header.
        command = b"\x01" + command

        socket.sendall(command)
        time.sleep(timeout)

        response = socket.recv(512)

        # Error handling for 9999FF1B, occurs when an invalid command is used.
        if b"FF1B" in response:
            response = b"Unrecognized function code. Use the command format form of the function."
        else:
            # Removes sent command from output.
            response = response[len(command)::]

        print(response)
