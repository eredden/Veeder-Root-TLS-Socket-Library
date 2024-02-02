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

    def execute(self, command: str, timeout: int) -> str:
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
        byte_command = start_of_header + bytes(command, "utf-8")

        is_display_command = command[0].isupper()
        invalid_command_error = b"FF1B"

        socket.sendall(byte_command)
        time.sleep(timeout)
        byte_response = socket.recv(65536)

        if invalid_command_error in byte_response:
            raise ValueError("Unrecognized function code. " \
                "Use the command format form of the function.")
        
        if not is_display_command:
            checksum_separator = b"&&"
            checksum_separator_position = byte_response[-7:-5]

            if checksum_separator not in checksum_separator_position:
                raise ValueError("Checksum missing from command response. " \
                    "Transmission either partially completed or failed.")

            if not data_integrity_check(byte_response):
                raise ValueError("Incorrect checksum, data integrity invalidated.")
        
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

def data_integrity_check(response: bytes) -> bool:
    """
    Verifies whether or not a command response retains its integrity
    after transmission by comparing it against the response checksum.

    response - Full command response up the checksum itself. Must include
    the start of header, command, response data, and the && separator.

    checksum - The checksum contained in-between the && separator and the
    end of transmission character.
    """

    response = response.decode()
    message = response[:-5]
    checksum = response[-5:-1]

    # calculate the 16-bit binary count of the message
    message_int = sum(ord(char) for char in message) & 0xFFFF

    # convert message integer to twos complement integer
    message_int = (message_int & 0xFFFF) + (message_int >> 16)
    message_int = message_int & 0xFFFF 

    # convert checksum hexadecimal string into integer
    checksum_int = int(checksum, 16)

    # compare sum of checksum and message to expected result
    integrity_threshold = "0b10000000000000000"
    binary_sum = bin(message_int + checksum_int)
    
    return bool(binary_sum == integrity_threshold)
