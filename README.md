# Veeder-Root ATG Socket Library

This is an unofficial wrapper for Python's socket library used for interacting with Veeder-Root's automatic tank gauging systems remotely through the Internet. This wrapper is primarily made to support the TLS-300 and TLS-350 and likely supports most functions of the TLS-450 as well.

If you believe there is something about this library that can be improved upon, please feel free to submit a issue or a pull request. I will do my best to respond to any inquiries promptly.

## Commands

The commands used to interact with Veeder-Root TLS-300/350/350R systems can be found in the "VEEDER - ROOT SERIAL INTERFACE MANUAL for TLS-300 and TLS-350 UST Monitoring Systems and TLS-350R Environmental & Inventory Management System" manual. You will want to look through Section 5 to get a better idea of how commands are sent, Section 6 to see how the responses are formatted, and Section 7 to see the available functions and their specific outputs.

You will want to use either the Computer or Display format of the function as listed under the Command Format header. For example, if you would like to use function code 101 (System Status Report) in the Display format, you would use the command ``I10100`` to do so. You do not need to add the start of header ``CTRL + A`` or ``\x01`` to the command as this is automatically prepended when using my wrapper. If your TLS system needs security codes in front of the commands, you can simply type the security code before the command like this: ``abcdefI10100``.

## Examples

This script demonstrates how you can programmatically connect to a TLS-350 system and get a system status report.

**Script:**

>```python
> from tls_socket_lib import tls_socket
>
> tls = tls_socket.tlsSocket("127.0.0.1", 10001) # initial connection
> response = tls.execute("i10100", 5) # get system status report
> 
> print(response) # print the response of the command
>```

**Output:**

>```python
> b'\x01i101002312301342020402&&FB3B\x03'
>```

This output shows the unaltered bytecode response from the TLS system. You can see the start of header ``\x01`` at the front, the command ``i10100`` we sent, the data ``2312301342020402``, then ``&&`` to separate the data from the checksum, ``FB3B``, and finally ``\x03`` showing the end of transmission.

You can remove some of the filler headers and footers from this code by running the output through tls_parser(). The only downside about this process is that the command has to be provided a second time here so that it can be removed from the ouput.

**Script:**

>```python
> results = tls_socket.tls_parser(response, "i10100")
> print(results)
>```

**Output:**

>```
> 2312301351020402&&FB3B
>```

You can see that the start of header ``\x01``, end of transmission ``\x03``, and the original command ``i10100`` have all been removed. Only the unique data is shown, and from here it can be split apart further to store the individual variables. For example, the first ten numbers here represent the date and time.

Review the "VEEDER - ROOT SERIAL INTERFACE MANUAL for TLS-300 and TLS-350 UST Monitoring Systems and TLS-350R Environmental & Inventory Management System" manual for information about how this response data is structured for each function.

# Using the TLS Client

You can also use the client.py file that I created for this library to interact with the TLS systems manually, similar to how you would with systems through Telnet, SSH, or Putty.

**Script:**

>```python
> python client.py "127.0.0.1" 10001
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
> 2312301229020402&&FB37
>
> >> I10100 
>
> DEC 30, 2023 12:29 PM
>
> GAS STATION
> 1234 GAS LANE
> HOUSTON, TX
> H07188463105001
>
> SYSTEM STATUS REPORT
>
> T 2:OVERFILL ALARM
>
> >>
> ```

By default, the output of these commands will be shown without the SOH, ETX, and original command. If you want to see the unaltered bytecode responses instead, use the ``--raw`` flag when initializing client.py.
