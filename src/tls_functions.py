import math
from tls_socket import tlsSocket
from tls_socket import tls_parser

def in_tank_inventory_report(tls: tlsSocket, timeout: int) -> dict:
    """
    Runs function 201 on a given Veeder-Root TLS device and returns a dict with report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.
    timeout - Time to wait for a response from the socket after executing the command.
    """

    command = "i20100"

    raw_output = tls.execute(command, timeout)
    output = tls_parser(raw_output, command)

    data = {}
    data["year"] = int(output[0:2])
    data["month"] = int(output[2:4])
    data["day"] = int(output[4:6])
    data["hour"] = int(output[6:8])
    data["minute"] = int(output[8:10])

    # split each tank report
    no_date_data = output[10:-6]
    split_data = []
    volume_length = 65

    for i, value in enumerate(no_date_data):
        array_position = math.floor(i / volume_length)

        if i % 65 == 0:
            split_data.append(value)
        else:
            split_data[array_position] = split_data[array_position] + value

    # strip values from within each individual report
    for value in split_data:
        tank_number = value[0:2]
        data["tank_" + tank_number] = {}
    
        tank_data = data["tank_" + tank_number]
        tank_data["product_code"] = value[2:3]
        tank_data["tank_status_bits"] = int(value[3:7])
        tank_data["eight_character_data_fields"] = int(value[7:9])
        tank_data["volume"] = value[9:17]
        tank_data["tc_volume"] = value[17:25]
        tank_data["ullage"] = value[25:33]
        tank_data["height"] = value[33:41]
        tank_data["water"] = value[41:49]
        tank_data["temperature"] = value[49:57]
        tank_data["water_volume"] = value[57:65]

    return data
