# async_socket.py - An asynchronous socket wrapper for TLS-3xx and TLS-4xx 
# devices manufactured by Veeder-Root.

import asyncio

class AsyncTLSSocket:
    """
    Defines an async socket for the TLS automatic tank gauges 
    manufactured by Veeder-Root.

    execute() - Used to send a command and view the output in accordance with 
    Veeder-Root Serial Interface Manual 576013-635.
    """

    def __init__(self, host: str, port: int = 10001, timeout: float = 4.0):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.reader = None
        self.writer = None

    # Allows usage of 'async with AsyncTLSSocket(...) as tls:'
    async def __aenter__(self):
        try:
            # Enforce the strict timeout on the initial connection.
            self.reader, self.writer = await asyncio.wait_for(
                asyncio.open_connection(self.host, self.port),
                timeout=self.timeout
            )

            return self
        
        except asyncio.TimeoutError:
            raise TimeoutError(f"[{self.host}] Connection timed out after {self.timeout} seconds.")

        except Exception as e:
            raise ConnectionError(f"[{self.host}] Connection failed: {e}")

    # Ensures the connection is cleanly closed upon exiting the block.
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()

    async def execute(self, 
                      command: str, 
                      etx: bytes = b"\x03") -> str:
        """
        Sends a command to a socket connection using the command 
        format from the Veeder-Root Serial Interface Manual 576013-635.

        command - The function code you would like to execute. 
        Make sure this is in computer format.

        etx - This has a default value (ASCII code 001) and should only be 
        changed if your ATG is set to use a different end of transmission.
        """
        
        if not self.writer or not self.reader:
            raise ConnectionError("Socket is not connected. Use 'async with' context.")

        # Validating function arguments prior to executing any commands.
        if not command:              raise ValueError("Argument 'command' cannot be empty.")
        if not type(command) == str: raise ValueError("Argument 'command' must be a string.")

        if not etx:                  raise ValueError("Argument 'etx' cannot be empty.")
        if not type(etx) == bytes:   raise ValueError("Argument 'etx' must be a bytecode.")

        # Setting up foundational variables.
        soh = b"\x01"
        end = b"\r\n" # Fixes an error when executing command i72E.

        # For the purposes of this socket, it doesn't make sense to ever use
        # display commands. We set the command to lowercase even if the user
        # explicitly uses I to indicate a display command. Use the synchronous
        # socket if you want the display command outputs.
        byte_command = soh + bytes(command.lower(), "utf-8") + end
        
        try:
            # Write non-blocking.
            self.writer.write(byte_command)
            await self.writer.drain()
            
            # Read non-blocking with a strict timeout.
            byte_response = await asyncio.wait_for(
                self.reader.readuntil(b'\x03'),
                timeout=self.timeout
            )
            
            return await self._handle_response(byte_response)
            
        except asyncio.TimeoutError:
            raise TimeoutError(f"[{self.host}] Read operation timed out.")
    
    async def _handle_response(self, byte_response: bytes) -> str:
        """
        Handles responses from the TLS system after executing a command.

        byte_response - Response from the TLS system.

        byte_command - The command that was executed to get the response.

        is_display - Used to determine if the command uses Display format.
        """

        # Validate that the generic error was not returned.
        if b"\x019999FF1B" in byte_response: 
            raise ValueError("Unsupported command for this server.")

        # Validate that the checksum is present and valid.
        checksum_separator = b"&&"
        checksum_separator_position  = byte_response[-7:-5]

        if checksum_separator not in checksum_separator_position:
            raise ValueError("Checksum missing from command response.")

        if not await self._data_integrity_check(byte_response):
            raise ValueError("Data integrity invalidated due to invalid checksum.")
        
        # Removes SOH, command, checksum, and ETX from being shown in output.
        response = byte_response.decode("utf-8")[7:][:-7]

        return response

    async def _data_integrity_check(self, byte_response: bytes) -> bool:
        """
        Verifies whether or not a command response retains its integrity
        after transmission by comparing it against the response checksum.

        response - Full command response up the checksum itself. Must include
        the start of header, command, response data, and the && separator.
        """

        response = byte_response.decode()
        message  = response[:-5]
        checksum = response[-5:-1]
        integrity_threshold = "0b10000000000000000"

        # Calculate the 16-bit binary count of the message.
        message_sum = sum(ord(char) for char in message) & 0xFFFF
        checksum_int = int(checksum, 16)

        # Compare sum of checksum and message to expected result.
        return bin(message_sum + checksum_int) == integrity_threshold