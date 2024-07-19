# socket.py - Defines the socket used to connect to TLS automatic tank gauges.

from time import sleep
import socket

class TlsSocket:
    """
    Defines a socket for the TLS automatic tank gauges 
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

    def execute(self, 
                command: str, 
                etx: bytes = b"\x03",
                retries: int = 30,
                timeout: int = 1,
                data_size: int = 4098) -> str:
        """
        Sends a command to a socket connection using the command 
        format from the Veeder-Root Serial Interface Manual 576013-635.

        command - The function code you would like to execute. 
        Make sure this is in computer format.

        etx - This has a default value (ASCII code 001) and should only be 
        changed if your ATG is set to use a different end of transmission.

        retries - The amount of times to listen for output before failing.

        timeout - The amount of time to listen per retry.

        data_size - The maximum amount of bytes to listen for at any time.
        """

        # Validating function arguments prior to executing any commands.
        if not command:              raise ValueError("Argument 'command' cannot be empty.")
        if not type(command) == str: raise ValueError("Argument 'command' must be a string.")

        if not etx:                  raise ValueError("Argument 'etx' cannot be empty.")
        if not type(etx) == bytes:   raise ValueError("Argument 'etx' must be a bytecode.")

        # Setting up foundational variables.
        socket = self.socket
        soh    = b"\x01"
        end    = b"\r\n" # Fixes an error when executing command i72E.

        byte_command = soh + bytes(command, "utf-8") + end
        is_display   = command[0].isupper()

        # Send command and repeatedly receive data in chunks until ETX is found.
        byte_response = b""

        socket.settimeout(timeout)
        socket.sendall(byte_command)

        for _ in range(0, retries):
            sleep(timeout)

            try:                 
                chunk = socket.recv(data_size)
                byte_response += chunk
                if chunk.endswith(etx): break

            except TimeoutError: 
                raise ValueError("Invalid command.")
    
        return self.__handle_response(byte_response, byte_command, is_display)
    
    def __handle_response(self, byte_response: bytes, 
                          byte_command: bytes, is_display: bool) -> str:
        """
        Handles responses from the TLS system after executing a command.

        byte_response - Response from the TLS system.

        byte_command - The command that was executed to get the response.

        is_display - Used to determine if the command uses Display format.
        """

        # Validate that the generic error was not returned.
        if b"\x019999FF1B" in byte_response: 
            raise ValueError("Unsupported command for this server.")

        # Check checksum position & value if non-Display format command is used.
        if is_display:
            # Removes SOH and ETX from being shown in output.
            response = byte_response.decode("utf-8")[1:][:-1]

            # Checks for and removes newlines at both ends of output.
            if response[:4]  == "\r\n\r\n": response = response[4:]
            if response[-4:] == "\r\n\r\n": response = response[:-4]
        else:
            checksum_separator = b"&&"
            checksum_separator_position  = byte_response[-7:-5]

            if checksum_separator not in checksum_separator_position:
                raise ValueError("Checksum missing from command response.")

            if not self.__data_integrity_check(byte_response):
                raise ValueError("Data integrity invalidated due to invalid checksum.")
            
            # Removes SOH, command, checksum, and ETX from being shown in output.
            response = byte_response.decode("utf-8")[7:][:-7]

        return response

    def __data_integrity_check(self, byte_response: bytes) -> bool:
        """
        Verifies whether or not a command response retains its integrity
        after transmission by comparing it against the response checksum.

        response - Full command response up the checksum itself. Must include
        the start of header, command, response data, and the && separator.
        """

        response = byte_response.decode()
        message  = response[:-5]
        checksum = response[-5:-1]

        # Calculate the 16-bit binary count of the message.
        message_int = sum(ord(char) for char in message) & 0xFFFF

        # Convert message integer to twos complement integer.
        message_int = message_int + (message_int >> 16)

        # Convert checksum hexadecimal string into integer.
        checksum_int = int(checksum, 16)

        # Compare sum of checksum and message to expected result.
        integrity_threshold = "0b10000000000000000"
        binary_sum = bin(message_int + checksum_int)
        
        return binary_sum == integrity_threshold