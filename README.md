# Veeder-Root TLS Socket Library

This is an unofficial wrapper for Python's socket library used for interacting with Veeder-Root's automatic tank gauging systems remotely through their serial interfaces. This wrapper is primarily made to support the TLS-300 and TLS-350 and may provide limited support for the TLS-450 as well.

If you believe there is something about this library that can be improved upon, please feel free to submit a issue or a pull request. I will do my best to respond to any inquiries promptly.

## Commands

The commands used to interact with Veeder-Root TLS-300/350/350R systems can be found in the "VEEDER - ROOT SERIAL INTERFACE MANUAL for TLS-300 and TLS-350 UST Monitoring Systems and TLS-350R Environmental & Inventory Management System" manual. You will want to look through Section 5.0 to get a better idea of how commands are sent and Section 6.0 to see how the responses are formatted.

After reading through those, you can find the available functions and commands in Section 7.0. You will want to use either the Computer or Display format of the command as listed under the Command Format header (note that the SOH is automatically added by this program). For example, if you would like to use function code 101 (System Status Report) in the Display format, you would use the command ``I10100`` to do so. See the below examples for more information about the outputs of these commands.

Section 7.0

## Examples

This script demonstrates how you can programmatically connect to a TLS-350 system and get a system status report. Note that the command in execute() is bytecode, not a string.

**Script:**

>```python
> from tls_socket_lib import tls_socket
>
> tls = tls_socket.tlsSocket("127.0.0.1", 10001) # initial connection
> tls.execute(b"i10100", 5) # get system status report, wait 5 seconds
>```

**Output:**

>```
> b'2312292336020402&&FB2F\x03'
>```

The functions and outputs created by the TLS systems can be understood by looking through the Veeder-Root Serial Interface Manual for the TSI-300/350/350R Monitoring Systems. I plan on adding a feature that converts the computer formatted output into more human-readable text in the future.

You can also use the client.py file that I created for this library to interact with the TLS systems manually, similar to how you would with systems through Telnet, SSH, or Putty.

**Script:**

>```python
> python client.py "127.0.0.1" 10001 --display_format
>```

**Output:**

>```
> You are connected to 127.0.0.1 using port 10001.
>
> >>
>```

From here, you can type in any function code to interact with the TLS system. As an example, you can type in ``I10100`` to output a system status report in display format, and ``i10100`` to display a system status report in computer format. The required start of header CTRL + A is automatically prepended to your command, so you do not need to worry about that.

> ```
> >> i10100
> ☺i101002312301113020402&&FB3F♥
> >> I10100
> ☺
> I10100
> DEC 30, 2023 11:13 AM
>
> GAS STATION
> 1234 GAS LANE
> HOUSTON, TEXAS
> H07188463105001
> 
> SYSTEM STATUS REPORT
> 
> T 2:OVERFILL ALARM
> 
> ♥
> ```

Note that the ``--display_format`` flag used when initializing the client does not dictate which format the command outputs, but is instead used to convert the bytecode output into string output. The case of the first letter dictates the true output format -- lowercase letters show computer format, uppercase letters show display format.

Another interesting topic would be the ☺ and ♥ that appear at the beginning and end of the output for both commands. These are UTF-8 representations of CTRL + A (the start of header for each command) and CTRL + C (the end of text character). These exclusively appear when the ``--display_format`` flag is used, and are shown as ``\x01`` and ``\x03`` in computer format.
