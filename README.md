# Veeder-Root TLS Socket Library

This is an unofficial wrapper for Python's socket library used for interacting with Veeder-Root's automatic tank gauging systems remotely through their serial interfaces. This wrapper is primarily made to support the TLS-300 and TLS-350 and may provide limited support for the TLS-450 as well.

If you believe there is something about this library that can be improved upon, please feel free to submit a issue or a pull request. I will do my best to respond to any inquiries promptly.

## Examples

This script demonstrates how you can remotely connect to a TLS-350 system and get a system status report. Note that the command in execute() is bytecode, not a string.

**Script:**

>```python
> import tls_socket
>
> tls = tls_socket.tlsSocket("127.0.0.1", 10001) # initial connection
> tls.execute(b"i10100", 5) # get system status report, wait 5 seconds
>```

**Output:**

>```
> b'2312292336020402&&FB2F\x03'
>```

The functions and outputs created by the TLS systems can be understood by looking through the Veeder-Root Serial Interface Manual for the TSI-300/350/350R Monitoring Systems. I plan on adding a feature that converts the computer formatted output into more human-readable text.
