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

    def execute(self, command: str, timeout: int, security_code = "") -> bytes:

        """
        Sends a command to a socket connection using the command format from the Veeder-Root Serial Interface Manual 576013-635.

        command - The function code you would like to execute. Make sure this is in computer format. \n
        timeout - The amount of time to wait for a response from the host. Adjust this as needed. \n
        display_format - Outputs values as strings instead of as bytecode.
        """

        socket = self.socket
        command = bytes(command, "utf-8")

        if validate_security_code(security_code):
            security_code = bytes(security_code, "utf-8")
        elif security_code == "":
            security_code = bytes(security_code, "utf-8")
        else:
            response = b"Invalid security code. Must be six characters long and use printable ASCII characters."
            print(response)
            return response
        

        # Appends CTRL + A as the start of header.
        command = b"\x01" + security_code + command

        # Send input, wait, receive output.
        socket.sendall(command)
        time.sleep(timeout)
        response = socket.recv(512)

        # Error handling when an invalid command is used (9999FF1B).
        if b"FF1B" in response:
            response = b"Unrecognized function code. Use the command format form of the function."
            print(response)
            return response

        return response

def remove_command_headers(response: bytes, command: str) -> str:
    """
    Takes output from any command and removes the SOH, originally sent command, and ETX.

    response - Response/output from a command ran with execute() from the tlsSocket class.
    command - The command used to get this output.
    """

    # Convert output to string.
    response = response.decode("utf-8")
    
    # Removes SOH, ETX, and command from being shown in output.
    # This works for both Computer and Display format commands.
    response = response[1:]
    response = response[:-1]
    response = response.replace(command, "")

    # Checks for newlines at both ends of output, removes if present.
    # Only applies to Display format commands.
    if response[:2] == "\r\n":
        response = response[2:]

    if response[-4:] == "\r\n\r\n":
        response = response[:-4]

    return response

def validate_security_code(security_code: str) -> bool:

    """
    Checks if the RS-232 security code meets length (6 characters) and character (printable ASCII) requirements.

    security_code - Security code used to authenticate to the TLS system.
    """

    # If a security code was not provided, simply return true.
    if security_code == None:
        return True

    # Check if security code uses ASCII characters.
    try:
        security_code.encode('ascii')
    except:
        return False
    
    # Ensure that security code length is six characters.
    if len(security_code) != 6:
        return False
    
    return True
