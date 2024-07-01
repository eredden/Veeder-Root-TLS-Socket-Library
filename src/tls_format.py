def get_timestamp(response: str) -> dict:
    """
    Extracts date and time from a automatic tank gauge command output/response.

    response - Output from the Veeder-Root TLS system.
    """

    return {
        "year":     int(response[0:2]),
        "month":    int(response[2:4]),
        "day":      int(response[4:6]),
        "hour":     int(response[6:8]),
        "minute":   int(response[8:10])
    }

def split_data(data: str, length: int) -> list:
    """
    Split a string into specified length chunks.

    data - The data to be split.

    length - The maximum length of each split chunk of data.
    """

    out = []

    for index in range(0, len(data), length):
        out.append(data[index:index + length])
    
    return out

def hex_to_float(hex: str) -> float:
    """
    Convert hexadecimal codes generated by the command responses into IEEE 
    floats.

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