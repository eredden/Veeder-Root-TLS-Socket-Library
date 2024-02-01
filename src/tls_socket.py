import socket
import time

class tlsSocket:
    """
    Defines a socket for the TLS-3XX automatic tank gauges 
    manufactured by Veeder-Root.

    execute() - Used to send a command and view the output in accordance with 
    Veeder-Root Serial Interface Manual 576013-635.
    """

    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port

        socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            socket_connection.connect((self.ip, self.port))
            self.socket = socket_connection
        
        except Exception as exception:
            raise exception
        
    def __str__(self):
        return f"tlsSocket({self.ip}, {self.port}, {self.socket})"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        socket = self.socket
        socket.close()

    def execute(self, byte_command: str, timeout: int) -> str:
        """
        Sends a command to a socket connection using the command 
        format from the Veeder-Root Serial Interface Manual 576013-635.

        command - The function code you would like to execute. 
        Make sure this is in computer format.

        timeout - The amount of time to wait for a response from the host. 
        Adjust this as needed.
        """

        socket = self.socket
        start_of_header = b"\x01"
        invalid_command_error = b"FF1B"
        
        byte_command = start_of_header + bytes(byte_command, "utf-8")

        socket.sendall(byte_command)
        time.sleep(timeout)
        byte_response = socket.recv(65536)

        if invalid_command_error in byte_response:
            response = "Unrecognized function code. " \
                "Use the command format form of the function."
            return response
        
        # removes SOH and ETX from being shown in output
        response = byte_response.decode("utf-8")[1:][:-1]
        command = byte_command.decode("utf-8")[1:]

        # Removes the command from being shown in output.
        response = response.replace(command, "")

        # checks for and removes newlines at both ends of output
        if response[:4] == "\r\n\r\n":
            response = response[4:]

        if response[-4:] == "\r\n\r\n":
            response = response[:-4]

        return response
