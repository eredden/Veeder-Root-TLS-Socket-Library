import math
from tls_socket import tlsSocket

def get_standard_values(output: str) -> dict:
    """
    Get standard values from a command response; date, time, checksum.

    output - Output of a command sent to a TLS system as a string.
    """

    data = {}

    data["year"] = int(output[0:2])
    data["month"] = int(output[2:4])
    data["day"] = int(output[4:6])
    data["hour"] = int(output[6:8])
    data["minute"] = int(output[8:10])
    data["checksum"] = output[-4:]

    return data

def hex_to_float(hex: str) -> float:
    """
    Convert hexadecimal codes generated by the command responses into IEEE floats.

    hex - An 8 character hexidecimal code stored as a string.
    """

    binary = ""

    for char in hex:
        hex_int = int(char, 16)
        hex_bin = format(hex_int, "04b")
        binary = binary + str(hex_bin)

    negative_int = int(binary[0], 2)
    negative = bool(negative_int)

    exponent_int = int(binary[1:9], 2)
    exponent = 2 ** (exponent_int - 127)

    mantissa_int = int(binary[9:], 2)
    mantissa_field = 2 ** 23
    mantissa = 1.0 + (mantissa_int / mantissa_field)

    if negative: exponent = -abs(exponent)

    decimal = round(exponent * mantissa, 5)

    return decimal

def function_101(tls: tlsSocket, tank: str, timeout: int) -> dict:
    """
    Runs function 101 on a given Veeder-Root TLS device and returns a dict with report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.
    tank - The tank number (ex. 00 for all tanks, 01 for tank one, etc).
    timeout - Time to wait for a response from the socket after executing the command.
    """

    command = "i101" + tank

    output = tls.execute(command, timeout)
    data = get_standard_values(output)

    # split tank reports
    data_without_date = output[10:-6]
    split_data = []
    volume_length = 6

    for i, value in enumerate(data_without_date):
        array_position = math.floor(i / volume_length)

        if i % volume_length == 0:
            split_data.append(value)
        else:
            split_data[array_position] = split_data[array_position] + value
    
    data["alarms"] = {}
    alarms = data["alarms"]
    
    for i, value in enumerate(split_data):
        alarm_number = str(i + 1)
        alarms["alarm_" + alarm_number] = {}

        alarm_data = alarms["alarm_" + alarm_number]
        alarm_data["alarm_category"] = value[0:2]
        alarm_data["alarm_type"] = value[2:4]
        alarm_data["tank_number"] = value[4:6]

    return data
        
def function_201(tls: tlsSocket, tank: str, timeout: int) -> dict:
    """
    Runs function 201 on a given Veeder-Root TLS device and returns a dict with report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.
    tank - The tank number (ex. 00 for all tanks, 01 for tank one, etc).
    timeout - Time to wait for a response from the socket after executing the command.
    """

    command = "i201" + tank

    output = tls.execute(command, timeout)
    data = get_standard_values(output)

    # split tank reports
    data_without_date = output[10:-6]
    split_data = []
    volume_length = 65

    for i, value in enumerate(data_without_date):
        array_position = math.floor(i / volume_length)

        if i % volume_length == 0:
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
