import math
from tls_socket import tlsSocket
from tls_socket import tls_parser, get_standard_values, hex_to_float

def function_201(tls: tlsSocket, tank: str, timeout: int) -> dict:
    """
    Runs function 201 on a given Veeder-Root TLS device and returns a dict with report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.
    tank - The tank number (ex. 00 for all tanks, 01 for tank one, etc).
    timeout - Time to wait for a response from the socket after executing the command.
    """

    command = "i201" + tank

    raw_output = tls.execute(command, timeout)
    output = tls_parser(raw_output, command)
    data = get_standard_values(output)

    # split tank reports
    data_without_date = output[10:-6]
    split_data = []
    volume_length = 65

    for i, value in enumerate(data_without_date):
        array_position = math.floor(i / volume_length)

        if i % 65 == 0:
            split_data.append(value)
        else:
            split_data[array_position] = split_data[array_position] + value

    # split values from within each individual tank report
    for value in split_data:
        tank_number = value[0:2]
        data["tank_" + tank_number] = {}
    
        tank_data = data["tank_" + tank_number]
        tank_data["product_code"] = value[2:3]
        tank_data["tank_status_bits"] = int(value[3:7])
        tank_data["volume"] = hex_to_float(value[9:17])
        tank_data["tc_volume"] = hex_to_float(value[17:25])
        tank_data["ullage"] = hex_to_float(value[25:33])
        tank_data["height"] = hex_to_float(value[33:41])
        tank_data["water"] = hex_to_float(value[41:49])
        tank_data["temperature"] = hex_to_float(value[49:57])
        tank_data["water_volume"] = hex_to_float(value[57:65])

    return data
