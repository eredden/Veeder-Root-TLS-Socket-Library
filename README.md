# Veeder-Root TLS Socket Library

This is an unofficial wrapper for Python's socket library used to interact with Veeder-Root's automatic tank gauges remotely through the Internet. This wrapper is primarily made to support the TLS-3xx and TLS-4xx series of automatic tank gauges.

If you believe there is something about this library that can be improved upon, please feel free to submit a issue or a pull request. I will do my best to respond to any inquiries promptly.

## Commands

The commands used to interact with Veeder-Root TLS-300/350/350R systems can be found in the [VEEDER - ROOT SERIAL INTERFACE MANUAL for TLS-300 and TLS-350 UST Monitoring Systems and TLS-350R Environmental & Inventory Management System](https://cdn.chipkin.com/files/liz/576013-635.pdf) manual. You will want to look through Section 5 to get a better idea of how commands are sent, Section 6 to see how the responses are formatted, and Section 7 to see the available functions and their specific outputs. This is exactly the same for the TLS-4xx series apart from the functions.

You will want to use either the Computer or Display format of the function as listed under the Command Format header. For example, if you would like to use function code 101 (System Status Report) in the Display format, you would use the command ``I10100`` to do so. You do not need to add the start of header ``CTRL + A`` to the command as this is automatically prepended when using my wrapper, as is the end of tranmission character ``CTRL + C``. If your TLS system needs security codes in front of the commands, then you would simply type the security code before the command.

## Examples

This script demonstrates how you can programmatically connect to an automatic tank gauge system and get a system status report.

**Script:**

>```python
> from tls_socket_lib import tls_socket
>
> tls = tls_socket.tlsSocket("127.0.0.1", 10001) # initial connection
> response = tls.execute("i10100", 3) # get system status report
> 
> print(response)
>```

**Output:**

>```python
> "2312301342020402&&FB3B"
>```

This output shows the response from the TLS system. The data ``2312301342020402``, separator ``&&``, and checksum ``FB3B`` are all provided to you through the ``execute()`` function as a string. You can see that the start of header ``\x01``, end of transmission ``\x03``, and the original command ``i10100`` have all been automatically removed by this library for your convenience.

Review the Veeder-Root Serial Interface manual provided with your model of automatic tank gauge for information about how response data is structured for each function. The serial interface manual for the TLS-3XX systems is linked at the beginning of this Markdown file.

# Using the TLS Client

You can also use the tls_client.py file that I created for this library to interact with the automatic tank gauge systems through a command line interface, similar to how you would with other systems through Telnet, SSH, or Putty.

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

From here, you can type in any function code to interact with the TLS system. As an example, you can type in ``I10100`` to output a system status report in display format, and ``i10100`` to display a system status report in computer format. The required start of header CTRL + A is automatically prepended to your command, so you do not need to worry about that.

> ```
> >> i10100
> 2312301229020402&&FB37
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

You may notice that a few of the responses from your TLS system do not fully appear. This can sometimes occur if the time between the program sending the command to the TLS system and listening back for it is too short, as these systems tend to have a bit of a delay with longer responses. This timeout is preset by default to one second to provide a fast experience out the box, and can be adjusted to wait longer by using the ``--timeout`` flag when executing tls_client.py. You need to enter an integer after this flag like ``3`` to indicate the amount of seconds to wait for a response.

## What's Next?

I am currently working on making more Pythonic functions for executing the commands on these TLS systems in tls_3xx_functions.py. These will be used to more easily store the response data from these functions as dict variables in Python programs. These functions are still being tested and should not be used in a production environment in their current state.
