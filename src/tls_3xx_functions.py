from tls_socket import tlsSocket

def get_standard_values(output: str) -> dict:
    """
    Get standard values from a command response; date, time, checksum. 
    Returns as a dict.

    output - Output of a command sent to a TLS system as a string.
    """

    return {
        "year":     int(output[0:2]),
        "month":    int(output[2:4]),
        "day":      int(output[4:6]),
        "hour":     int(output[6:8]),
        "minute":   int(output[8:10]),
        "checksum": output[-4:]
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

def function_101(tls: tlsSocket, tank: str) -> dict:
    """
    Runs function 101 on a given Veeder-Root TLS device and returns a dict with 
    report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.

    tank - The tank number (ex. 00 for all tanks, 01 for tank one, etc).
    """

    # Execute the command and extract common values from it immediately.
    response = tls.execute("i101" + tank)    
    data = get_standard_values(response)

    # Get values from the remaining data, split up alarms.
    remaining_data = response[10:-6]
    data_length = 6

    if len(remaining_data) < data_length: 
        return data
    
    split_remaining_data = split_data(remaining_data, data_length)
    
    # Get values from within each individual alarm.
    data["alarms"] = []

    for value in split_remaining_data:
        data["alarms"].append({
            "alarm_category": int(value[0:2]),
            "alarm_type":     int(value[2:4]),
            "tank_number":    int(value[4:6])
        })

    return data
        
def function_102(tls: tlsSocket) -> dict:
    """
    Runs function 102 on a given Veeder-Root TLS device and returns a dict with 
    report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.
    """

    command = "i10200"
    response = tls.execute(command)    
    data = get_standard_values(response)

    # Strip generic values from data, then split into individual chunks.
    remaining_data = response[12:-6]
    expected_data_length = 20
    split_remaining_data = split_data(remaining_data, expected_data_length)

    data["slots"] = {}
    slots = data["slots"]

    if len(remaining_data) < expected_data_length: return data

    # Split values from within each individual tank report.
    for i, value in enumerate(split_remaining_data):
        slot_number = str(i + 1)
        slots["slot_" + slot_number] = {}
    
        slot_data = slots["slot_" + slot_number]
        slot_data["type_of_module"] = value[2:4]
        slot_data["power_on_reset"] = hex_to_float(value[4:12])
        slot_data["current_io_reading"] = hex_to_float(value[12:19])

    return data

def function_111(tls: tlsSocket) -> dict:
    """
    Runs function 111 on a given Veeder-Root TLS device and returns a dict with 
    report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.
    """

    command = "i11100"
    response = tls.execute(command)    
    data = get_standard_values(response)

    # Strip generic values from data, then split into individual chunks.
    remaining_data = response[10:-6]
    expected_data_length = 20
    split_remaining_data = split_data(remaining_data, expected_data_length)

    data["alarms"] = {}
    alarms = data["alarms"]

    if len(remaining_data) < expected_data_length: return data

    # Split values from within each individual tank report.
    for i, value in enumerate(split_remaining_data):
        alarm_number = str(i + 1)
        alarms["alarm_" + alarm_number] = {}
    
        alarm_data = alarms["alarm_" + alarm_number]
        alarm_data["alarm_category"] = int(value[0:2])
        alarm_data["sensor_category"] = int(value[2:4])
        alarm_data["alarm_type"] = int(value[4:6])
        alarm_data["tank_number"] = int(value[6:8])
        alarm_data["alarm_state"] = int(value[8:10])
        alarm_data["year"] = int(value[10:12])
        alarm_data["month"] = int(value[12:14])
        alarm_data["day"] = int(value[14:16])
        alarm_data["hour"] = int(value[16:18])
        alarm_data["minute"] = int(value[18:20])

    return data

def function_112(tls: tlsSocket) -> dict:
    """
    Runs function 112 on a given Veeder-Root TLS device and returns a dict with 
    report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.
    """

    command = "i11200"
    response = tls.execute(command)    
    data = get_standard_values(response)

    # Strip generic values from data, then split into individual chunks.
    remaining_data = response[10:-6]
    expected_data_length = 20
    split_remaining_data = split_data(remaining_data, expected_data_length)

    data["alarms"] = {}
    alarms = data["alarms"]

    if len(remaining_data) < expected_data_length: return data

    # Split values from within each individual tank report.
    for i, value in enumerate(split_remaining_data):
        alarm_number = str(i + 1)
        alarms["alarm_" + alarm_number] = {}
    
        alarm_data = alarms["alarm_" + alarm_number]
        alarm_data["alarm_category"] = int(value[0:2])
        alarm_data["sensor_category"] = int(value[2:4])
        alarm_data["alarm_type"] = int(value[4:6])
        alarm_data["tank_number"] = int(value[6:8])
        alarm_data["alarm_state"] = int(value[8:10])
        alarm_data["year"] = int(value[10:12])
        alarm_data["month"] = int(value[12:14])
        alarm_data["day"] = int(value[14:16])
        alarm_data["hour"] = int(value[16:18])
        alarm_data["minute"] = int(value[18:20])

    return data

def function_113(tls: tlsSocket) -> dict:
    """
    Runs function 113 on a given Veeder-Root TLS device and returns a dict with 
    report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.
    """

    command = "i11300"
    response = tls.execute(command)
    data = get_standard_values(response)

    # Store extra non-repeated info from this response.
    data["station_header_1"] = response[10:30].strip()
    data["station_header_2"] = response[30:50].strip()
    data["station_header_3"] = response[50:70].strip()
    data["station_header_4"] = response[70:90].strip()

    # Strip generic values from data, then split into individual chunks.
    remaining_data = response[90:-6]
    expected_data_length = 18
    split_remaining_data = split_data(remaining_data, expected_data_length)

    data["alarms"] = {}
    alarms = data["alarms"]

    if len(remaining_data) < expected_data_length: return data

    # Split values from within each individual tank report.
    for i, value in enumerate(split_remaining_data):
        alarm_number = str(i + 1)
        alarms["alarm_" + alarm_number] = {}
    
        alarm_data = alarms["alarm_" + alarm_number]
        alarm_data["alarm_category"] = int(value[0:2])
        alarm_data["sensor_category"] = int(value[2:4])
        alarm_data["alarm_type"] = int(value[4:6])
        alarm_data["tank_number"] = int(value[6:8])
        alarm_data["year"] = int(value[8:10])
        alarm_data["month"] = int(value[10:12])
        alarm_data["day"] = int(value[12:14])
        alarm_data["hour"] = int(value[14:16])
        alarm_data["minute"] = int(value[16:18])

    return data

def function_114(tls: tlsSocket) -> dict:
    """
    Runs function 114 on a given Veeder-Root TLS device and returns a dict with 
    report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.
    """

    command = "i11400"
    response = tls.execute(command)    
    data = get_standard_values(response)

    # Store extra non-repeated info from this response.
    data["station_header_1"] = response[10:30].strip()
    data["station_header_2"] = response[30:50].strip()
    data["station_header_3"] = response[50:70].strip()
    data["station_header_4"] = response[70:90].strip()

    # Strip generic values from data, then split into individual chunks.
    remaining_data = response[90:-6]
    expected_data_length = 20
    split_remaining_data = split_data(remaining_data, expected_data_length)

    data["alarms"] = {}
    alarms = data["alarms"]

    if len(remaining_data) < expected_data_length: return data

    # Split values from within each individual tank report.
    for i, value in enumerate(split_remaining_data):
        alarm_number = str(i + 1)
        alarms["alarm_" + alarm_number] = {}
    
        alarm_data = alarms["alarm_" + alarm_number]
        alarm_data["alarm_category"] = int(value[0:2])
        alarm_data["sensor_category"] = int(value[2:4])
        alarm_data["alarm_type"] = int(value[4:6])
        alarm_data["tank_number"] = int(value[6:8])
        alarm_data["alarm_state"] = int(value[8:10])
        alarm_data["year"] = int(value[10:12])
        alarm_data["month"] = int(value[12:14])
        alarm_data["day"] = int(value[14:16])
        alarm_data["hour"] = int(value[16:18])
        alarm_data["minute"] = int(value[18:20])

    return data

def function_115(tls: tlsSocket) -> dict:
    """
    Runs function 115 on a given Veeder-Root TLS device and returns a dict with 
    report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.
    """

    command = "i11500"
    response = tls.execute(command)    
    data = get_standard_values(response)

    # Store extra non-repeated info from this response.
    data["station_header_1"] = response[10:30].strip()
    data["station_header_2"] = response[30:50].strip()
    data["station_header_3"] = response[50:70].strip()
    data["station_header_4"] = response[70:90].strip()

    # Strip generic values from data, then split into individual chunks.
    remaining_data = response[90:-6]
    expected_data_length = 18
    split_remaining_data = split_data(remaining_data, expected_data_length)

    data["alarms"] = {}
    alarms = data["alarms"]

    if len(remaining_data) < expected_data_length: return data

    # Split values from within each individual tank report.
    for i, value in enumerate(split_remaining_data):
        alarm_number = str(i + 1)
        alarms["alarm_" + alarm_number] = {}
    
        alarm_data = alarms["alarm_" + alarm_number]
        alarm_data["alarm_category"] = int(value[0:2])
        alarm_data["sensor_category"] = int(value[2:4])
        alarm_data["alarm_type"] = int(value[4:6])
        alarm_data["tank_number"] = int(value[6:8])
        alarm_data["year"] = int(value[8:10])
        alarm_data["month"] = int(value[10:12])
        alarm_data["day"] = int(value[12:14])
        alarm_data["hour"] = int(value[14:16])
        alarm_data["minute"] = int(value[16:18])

    return data

def function_116(tls: tlsSocket) -> dict:
    """
    Runs function 116 on a given Veeder-Root TLS device and returns a dict with 
    report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.
    """

    command = "i11600"
    response = tls.execute(command)    
    data = get_standard_values(response)

    # Store extra non-repeated info from this response.
    data["station_header_1"] = response[10:30].strip()
    data["station_header_2"] = response[30:50].strip()
    data["station_header_3"] = response[50:70].strip()
    data["station_header_4"] = response[70:90].strip()
    data["number_of_records"] = int(response[90:92])

    # Strip generic values from data, then split into individual chunks.
    remaining_data = response[90:-6]
    expected_data_length = 25
    split_remaining_data = split_data(remaining_data, expected_data_length)

    data["reports"] = {}
    reports = data["reports"]

    if len(remaining_data) < expected_data_length: return data

    # Split values from within each individual tank report.
    for i, value in enumerate(split_remaining_data):
        report_number = str(i + 1)
        reports["report_" + report_number] = {}
    
        report_data = reports["report_" + report_number]
        report_data["year"] = int(value[0:2])
        report_data["month"] = int(value[2:4])
        report_data["day"] = int(value[4:6])
        report_data["hour"] = int(value[6:8])
        report_data["minute"] = int(value[8:10])
        report_data["service_id"] = value[10:20].strip()
        report_data["service_code"] = value[20:25].strip()

    return data

def function_119(tls: tlsSocket, start_date: str, end_date: str) -> dict:
    """
    Runs function 119 on a given Veeder-Root TLS device and returns a dict with 
    report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.

    start_date - The beginning of the range of time to look through with this 
    command (yymmdd format).

    end_date - The end of the range of time to look through with this command 
    (yymmdd format).
    """

    # This command can take a date range optionally.
    if start_date != "" and end_date != "":
        command = "i11900" + start_date + end_date
    else: command = "i11900"

    response = tls.execute(command)    
    data = get_standard_values(response)

    # Store extra non-repeated info from this response.
    data["number_of_records"] = int(response[10:14])

    # Strip generic values from data, then split into individual chunks.
    remaining_data = response[14:-6]
    expected_data_length = 18
    split_remaining_data = split_data(remaining_data, expected_data_length)

    data["records"] = {}
    records = data["records"]

    if len(remaining_data) < expected_data_length: return data

    # Split values from within each individual tank report.
    for i, value in enumerate(split_remaining_data):
        record_number = str(i + 1)
        records["record_" + record_number] = {}
    
        record_data = records["record_" + record_number]
        record_data["year"] = int(value[0:2])
        record_data["month"] = int(value[2:4])
        record_data["day"] = int(value[4:6])
        record_data["hour"] = int(value[6:8])
        record_data["minute"] = int(value[8:10])
        record_data["record_type"] = value[10:12]
        record_data["data_field"] = value[12:18]

    return data

def function_11A(tls: tlsSocket) -> dict:
    """
    Runs function 11A on a given Veeder-Root TLS device and returns a dict with 
    report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.
    """

    command = "i11A00"
    response = tls.execute(command)    
    data = get_standard_values(response)

    # Store extra non-repeated info from this response.
    data["number_of_records"] = int(response[10:12])

    # Strip generic values from data, then split into individual chunks.
    remaining_data = response[12:-6]
    expected_data_length = 20
    split_remaining_data = split_data(remaining_data, expected_data_length)

    data["reports"] = {}
    reports = data["reports"]

    if len(remaining_data) < expected_data_length: return data

    # Split values from within each individual tank report.
    for i, value in enumerate(split_remaining_data):
        report_number = str(i + 1)
        reports["report_" + report_number] = {}
    
        report_data = reports["report_" + report_number]
        report_data["year"] = int(value[0:2])
        report_data["month"] = int(value[2:4])
        report_data["day"] = int(value[4:6])
        report_data["hour"] = int(value[6:8])
        report_data["minute"] = int(value[8:10])
        report_data["service_id"] = value[10:16].strip()
        report_data["service_code"] = value[16:20].strip()

    return data

def function_11B(tls: tlsSocket) -> dict:
    """
    Runs function 11B on a given Veeder-Root TLS device and returns a dict with 
    report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.
    """

    command = "i11B00"
    response = tls.execute(command)    
    data = get_standard_values(response)

    # Store extra non-repeated info from this response.
    data["service_notice_session"] = int(response[10:11])
    data["start_year"] = int(response[11:13])
    data["start_month"] = int(response[13:15])
    data["start_day"] = int(response[15:17])
    data["start_hour"] = int(response[17:19])
    data["start_minute"] = int(response[19:21])
    data["number_of_records"] = int(response[21:23], 16)

    # Strip generic values from data, then split into individual chunks.
    remaining_data = response[23:-6]
    expected_data_length = 20
    split_remaining_data = split_data(remaining_data, expected_data_length)

    data["reports"] = {}
    reports = data["reports"]

    if len(remaining_data) < expected_data_length: return data

    # Split values from within each individual tank report.
    for i, value in enumerate(split_remaining_data):
        report_number = str(i + 1)
        reports["report_" + report_number] = {}
    
        report_data = reports["report_" + report_number]
        report_data["start_year"] = int(value[0:2])
        report_data["start_month"] = int(value[2:4])
        report_data["start_day"] = int(value[4:6])
        report_data["start_hour"] = int(value[6:8])
        report_data["start_minute"] = int(value[8:10])
        report_data["end_year"] = int(value[10:12])
        report_data["end_month"] = int(value[12:14])
        report_data["end_day"] = int(value[14:16])
        report_data["end_hour"] = int(value[16:18])
        report_data["end_minute"] = int(value[18:20])

    return data

def function_201(tls: tlsSocket, tank: str) -> dict:
    """
    Runs function 201 on a given Veeder-Root TLS device and returns a dict with 
    report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.

    tank - The tank number (ex. 00 for all tanks, 01 for tank one, etc).
    """

    command = "i201" + tank
    response = tls.execute(command)    
    data = get_standard_values(response)

    # Strip generic values from data, then split into individual chunks.
    remaining_data = response[10:-6]
    expected_data_length = 65
    split_remaining_data = split_data(remaining_data, expected_data_length)

    if len(remaining_data) < expected_data_length: return data

    # Split values from within each individual tank report.
    for value in split_remaining_data:
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

# NON-FUNCTIONAL, still being worked on due to checksum issues.
def function_202(tls: tlsSocket, tank: str) -> dict:
    """
    Runs function 202 on a given Veeder-Root TLS device and returns a dict with 
    report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.

    tank - The tank number (ex. 00 for all tanks, 01 for tank one, etc).
    """

    command = "i202" + tank
    response = tls.execute(command)    
    data = get_standard_values(response)

    # Strip generic values from data, then split into individual chunks.
    remaining_data = response[10:-6]
    expected_data_length = 107
    split_remaining_data = split_data(remaining_data, expected_data_length)

    if len(remaining_data) < expected_data_length: return data

    # Split values from within each individual tank report.
    for value in split_remaining_data:
        tank_number = value[0:2]
        data["tank_" + tank_number] = {}
    
        tank_data = data["tank_" + tank_number]
        tank_data["product_code"] = value[2:3]
        tank_data["number_of_deliveries"] = int(value[3:5])
        tank_data["start_year"] = int(value[5:7])
        tank_data["start_month"] = int(value[7:9])
        tank_data["start_day"] = int(value[9:11])
        tank_data["start_hour"] = int(value[11:13])
        tank_data["start_minute"] = int(value[13:15])
        tank_data["end_year"] = int(value[15:17])
        tank_data["end_month"] = int(value[17:19])
        tank_data["end_day"] = int(value[19:21])
        tank_data["end_hour"] = int(value[21:23])
        tank_data["end_minute"] = int(value[23:25])
        tank_data["starting_volume"] = hex_to_float(value[27:35])
        tank_data["starting_tc_volume"] = hex_to_float(value[35:43])
        tank_data["starting_water"] = hex_to_float(value[43:51])
        tank_data["starting_temp"] = hex_to_float(value[51:59])
        tank_data["ending_volume"] = hex_to_float(value[59:67])
        tank_data["ending_tc_volume"] = hex_to_float(value[67:75])
        tank_data["ending_water"] = hex_to_float(value[75:83])
        tank_data["ending_temp"] = hex_to_float(value[83:91])
        tank_data["starting_height"] = hex_to_float(value[91:99])
        tank_data["ending_height"] = hex_to_float(value[99:107])

    return data
