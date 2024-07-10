# Veeder-Root TLS Socket Library

This is an unofficial Python sockets wrapper for querying Veeder-Root automatic tank gauges remotely 
through the Internet. This wrapper is primarily made to support the TLS-3xx and TLS-4xx series of 
automatic tank gauges.

If you believe there is something about this library that can be improved upon, please feel free to 
submit a issue or a pull request. I will do my best to respond to any inquiries promptly.

## Commands

The commands used to interact with Veeder-Root TLS-4XX series systems can be found in the Serial 
Interface Manual in the `docs` directory of this repository. You will want to look through Section 5
 to get a better idea of how commands are sent, Section 6 to see how the responses are formatted, 
 and Section 7 to see the available functions and their specific outputs. This is exactly the same 
 for the TLS-3XX series apart from the available functions.

You will want to use either the Computer or Display format of the function as listed under the 
Command Format header. For example, if you would like to use function code 101 (System Status 
Report) in the Display format, you would use the command ``I10100`` to do so. You do not need 
to add the start of header ``CTRL + A`` to the command as this is automatically prepended when 
using my wrapper, as is the end of tranmission character ``CTRL + C``. If your TLS system needs 
security codes in front of the commands, then you would simply type the security code before the 
command.

## Examples

This script demonstrates how you can programmatically connect to an automatic tank gauge system and 
get a system status report.

**Script:**

>```python
> from veeder_root_tls_socket_library.socket import TlsSocket
>
> tls = TlsSocket("127.0.0.1", 10001) # initial connection
> response = tls.execute("i10100") # get system status report
> 
> print(response)
>```

**Output:**

>```python
> "2312301342020402"
>```

This output shows the response from the TLS system. The data ``2312301342020402`` is provided to you
 through the ``execute()`` function as a string. You can see that the start of header ``\x01``, the 
 original command ``i10100``,  the checksum separator ``&&``, the checksum ``FB3B``, and the end of 
 transmission ``\x03`` have all been automatically stripped from the output for your convenience. 
 The checksum is automatically checked against the output and a ``ValueError`` is produced if the 
 integrity check fails.

Review the Veeder-Root Serial Interface manual provided with your model of automatic tank gauge for 
information about how response data is structured for each function. The serial interface manual for
 the TLS-4XX systems is linked at the beginning of this Markdown file.

# Using the TLS Client

You can also use the ``tls_client.py`` file that I created for this library to interact with the 
automatic tank gauge systems through a command line interface, similar to how you would with other 
systems through Telnet, SSH, or Putty.

**Script:**

>```python
> python tls_client.py "127.0.0.1" 10001
>```

**Output:**

>```
> You are connected to 127.0.0.1 using port 10001.
>
> >>
>```

From here, you can type in any function code to interact with the TLS system. As an example, you can
 type in ``I10100`` to output a system status report in display format, and ``i10100`` to display a 
 system status report in computer format. The required start of header CTRL + A is automatically 
 prepended to your command, so you do not need to worry about that.

> ```
> >> i10100
> 2312301229020402
>
> >> I10100 
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

The time between responses will vary based on how large the responses are. The response for a 
command like `i10100` will be significantly smaller than that of `I11100`. I have implemented a 
dynamic waiting function to stop receiving response data once the end of transmission character 
is hit. If this is not hit, the program will continue to wait for thirty seconds and will raise 
an error after that point.

## Using The TLS-3XX Functions

I have also created various functions that can be used to 
query information from TLS-3XX systems and output a Python dict object rather than the raw output 
that is typically given by these systems. This serves well for extracting specific bits of data from
 these commands (e.g. the ullage of a specific tank).

**Script:**

> ```python
> from veeder_root_tls_socket_library.socket import TlsSocket
> from veeder_root_tls_socket_library import tls_3xx
>
> # initial connection
> tls = TlsSocket("127.0.0.1", 10001) 
> # function_101() used instead of execute("i10100")
> response = tls_3xx.function_101(tls, "00")
>
> print(response)
> ```

**Output:**

> ```python
> {
>   'year': 24, 
>   'month': 5,
>   'day': 26,
>   'hour': 16,
>   'minute': 14,
>   'alarms': [{'alarm_category': 2, 'alarm_type': 5, 'tank_number': '01'}]
> }
> ```

This looks much more readable than a string of numbers! By using these dedicated functions, you can 
have this data more readily accessible through a Python `dict` object. Another notable upside of 
this is that strings and floats are converted by these functions as well, so you do not have to 
worry about implementing your own IEEE-compliant hex to float function like I did.

The downside of this is that not every TLS-3XX function code has been added yet. Please feel free to 
submit a feature request or pull request with additional functions if you would like them added 
to my library.
