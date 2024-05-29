from tls_socket import tlsSocket

def get_standard_values(output: str) -> dict:
    """
    Get standard values such as date and time from a command response.
    Returns as a dict.

    output - Output of a command sent from a TLS system.
    """

    return {
        "year":     int(output[0:2]),
        "month":    int(output[2:4]),
        "day":      int(output[4:6]),
        "hour":     int(output[6:8]),
        "minute":   int(output[8:10])
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
    
    data["alarms"] = []

    # Get values from the remaining data, split up alarms.
    remaining_data = response[10:]
    data_length = 6

    if len(remaining_data) < data_length: 
        return data
    
    split_remaining_data = split_data(remaining_data, data_length)
    
    # Get values from each alarm.
    for value in split_remaining_data:
        data["alarms"].append({
            "alarm_category": int(value[0:2]),
            "alarm_type":     int(value[2:4]),
            "tank_number":    value[4:6]
        })

    return data
        
def function_102(tls: tlsSocket) -> dict:
    """
    Runs function 102 on a given Veeder-Root TLS device and returns a dict with 
    report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.
    """

    # Execute the command and extract common values from it immediately.
    response = tls.execute("i10200")    
    data = get_standard_values(response)
    
    data["slots"] = []

    # Get values from the remaining data, split up slots.
    remaining_data = response[12:]
    expected_data_length = 20

    if len(remaining_data) < expected_data_length: 
        return data
    
    split_remaining_data = split_data(remaining_data, expected_data_length)

    # Get values from each slot.
    for value in split_remaining_data:
        data["slots"].append({
            "slot_number":        int(value[0:2], 16),
            "type_of_module":     value[2:4],
            "power_on_reset":     hex_to_float(value[4:12]),
            "current_io_reading": hex_to_float(value[12:19])
        })

    return data

def function_111(tls: tlsSocket) -> dict:
    """
    Runs function 111 on a given Veeder-Root TLS device and returns a dict with 
    report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.
    """

    # Execute the command and extract common values from it immediately.
    response = tls.execute("i11100")    
    data = get_standard_values(response)
    
    data["alarms"] = []

    # Get values from the remaining data, split up alarms.
    remaining_data = response[10:]
    expected_data_length = 20

    if len(remaining_data) < expected_data_length: 
        return data

    split_remaining_data = split_data(remaining_data, expected_data_length)

    # Get values from each alarm.
    for value in split_remaining_data:
        data["alarms"].append({
            "alarm_category":  int(value[0:2]),
            "sensor_category": int(value[2:4]),
            "alarm_type":      int(value[4:6]),
            "tank_number":     value[6:8],
            "alarm_state":     int(value[8:10]),
            "year":            int(value[10:12]),
            "month":           int(value[12:14]),
            "day":             int(value[14:16]),
            "hour":            int(value[16:18]),
            "minute":          int(value[18:20])
        })
        
    return data

def function_112(tls: tlsSocket) -> dict:
    """
    Runs function 112 on a given Veeder-Root TLS device and returns a dict with 
    report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.
    """

    # Execute the command and extract common values from it immediately.
    response = tls.execute("i11200")    
    data = get_standard_values(response)
    
    data["alarms"] = []

    # Get values from the remaining data, split up alarms.
    remaining_data = response[10:]
    expected_data_length = 20

    if len(remaining_data) < expected_data_length: 
        return data

    split_remaining_data = split_data(remaining_data, expected_data_length)
    
    # Get values from each alarm.
    for value in split_remaining_data:
        data["alarms"].append({
            "alarm_category":  int(value[0:2]),
            "sensor_category": int(value[2:4]),
            "alarm_type":      int(value[4:6]),
            "tank_number":     value[6:8],
            "alarm_state":     int(value[8:10]),
            "year":            int(value[10:12]),
            "month":           int(value[12:14]),
            "day":             int(value[14:16]),
            "hour":            int(value[16:18]),
            "minute":          int(value[18:20])
        })
    
    return data

def function_113(tls: tlsSocket) -> dict:
    """
    Runs function 113 on a given Veeder-Root TLS device and returns a dict with 
    report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.
    """

    # Execute the command and extract common values from it immediately.
    response = tls.execute("i11300")
    data = get_standard_values(response)

    # Store extra non-repeated info from this response.
    data["station_header_1"] = response[10:30].strip()
    data["station_header_2"] = response[30:50].strip()
    data["station_header_3"] = response[50:70].strip()
    data["station_header_4"] = response[70:90].strip()
    
    data["alarms"] = []

    # Get values from the remaining data, split up alarms.
    remaining_data = response[90:]
    expected_data_length = 18

    if len(remaining_data) < expected_data_length: 
        return data

    split_remaining_data = split_data(remaining_data, expected_data_length)

    # Get values from each alarm.
    for value in split_remaining_data:
        data["alarms"].append({
            "alarm_category":  int(value[0:2]),
            "sensor_category": int(value[2:4]),
            "alarm_type":      int(value[4:6]),
            "tank_number":     value[6:8],
            "year":            int(value[8:10]),
            "month":           int(value[10:12]),
            "day":             int(value[12:14]),
            "hour":            int(value[14:16]),
            "minute":          int(value[16:18])
        })    

    return data

def function_114(tls: tlsSocket) -> dict:
    """
    Runs function 114 on a given Veeder-Root TLS device and returns a dict with 
    report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.
    """

    # Execute the command and extract common values from it immediately.
    response = tls.execute("i11400")    
    data = get_standard_values(response)

    # Store extra non-repeated info from this response.
    data["station_header_1"] = response[10:30].strip()
    data["station_header_2"] = response[30:50].strip()
    data["station_header_3"] = response[50:70].strip()
    data["station_header_4"] = response[70:90].strip()
    
    data["alarms"] = []

    # Get values from the remaining data, split up alarms.
    remaining_data = response[90:]
    expected_data_length = 20

    if len(remaining_data) < expected_data_length: 
        return data
    
    split_remaining_data = split_data(remaining_data, expected_data_length)

    # Get values from each alarm.
    for value in split_remaining_data:
        data["alarms"].append({
            "alarm_category":  int(value[0:2]),
            "sensor_category": int(value[2:4]),
            "alarm_type":      int(value[4:6]),
            "tank_number":     value[6:8],
            "alarm_state":     int(value[8:10]),
            "year":            int(value[10:12]),
            "month":           int(value[12:14]),
            "day":             int(value[14:16]),
            "hour":            int(value[16:18]),
            "minute":          int(value[18:20])
        })

    return data

def function_115(tls: tlsSocket) -> dict:
    """
    Runs function 115 on a given Veeder-Root TLS device and returns a dict with 
    report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.
    """

    # Execute the command and extract common values from it immediately.
    response = tls.execute("i11500")    
    data = get_standard_values(response)

    # Store extra non-repeated info from this response.
    data["station_header_1"] = response[10:30].strip()
    data["station_header_2"] = response[30:50].strip()
    data["station_header_3"] = response[50:70].strip()
    data["station_header_4"] = response[70:90].strip()

    data["alarms"] = []

    # Get values from the remaining data, split up alarms.
    remaining_data = response[90:]
    expected_data_length = 18

    if len(remaining_data) < expected_data_length: 
        return data
    
    split_remaining_data = split_data(remaining_data, expected_data_length)

    # Get values from each alarm.
    for value in split_remaining_data:
        data["alarms"].append({
            "alarm_category":  int(value[0:2]),
            "sensor_category": int(value[2:4]),
            "alarm_type":      int(value[4:6]),
            "tank_number":     value[6:8],
            "year":            int(value[8:10]),
            "month":           int(value[10:12]),
            "day":             int(value[12:14]),
            "hour":            int(value[14:16]),
            "minute":          int(value[16:18])
        })

    return data

def function_116(tls: tlsSocket) -> dict:
    """
    Runs function 116 on a given Veeder-Root TLS device and returns a dict with 
    report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.
    """

    # Execute the command and extract common values from it immediately.
    response = tls.execute("i11600")    
    data = get_standard_values(response)

    # Store extra non-repeated info from this response.
    data["station_header_1"] =  response[10:30].strip()
    data["station_header_2"] =  response[30:50].strip()
    data["station_header_3"] =  response[50:70].strip()
    data["station_header_4"] =  response[70:90].strip()
    data["number_of_records"] = int(response[90:92])

    data["reports"] = []

    # Get values from the remaining data, split up reports.
    remaining_data = response[90:]
    expected_data_length = 25
    
    if len(remaining_data) < expected_data_length: 
        return data
    
    split_remaining_data = split_data(remaining_data, expected_data_length)

    # Get values from each reports.
    for value in split_remaining_data:
        data["reports"].append({
            "year":         int(value[0:2]),
            "month":        int(value[2:4]),
            "day":          int(value[4:6]),
            "hour":         int(value[6:8]),
            "minute":       int(value[8:10]),
            "service_id":   value[10:20].strip(),
            "service_code": value[20:25].strip()
        })
        
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

    # Execute the command and extract common values from it immediately.
    if start_date != "" and end_date != "":
        response = tls.execute("i11900" + start_date + end_date) 
    else: 
        response = tls.execute("i11900")

    data = get_standard_values(response)

    # Store extra non-repeated info from this response.
    data["number_of_records"] = int(response[10:14])
    data["records"] = []

    # Get values from the remaining data, split up records.
    remaining_data = response[14:]
    expected_data_length = 18

    if len(remaining_data) < expected_data_length: 
        return data

    split_remaining_data = split_data(remaining_data, expected_data_length)

    # Get values from each record.
    for value in split_remaining_data:
        data["records"].append({
            "year":        int(value[0:2]),
            "month":       int(value[2:4]),
            "day":         int(value[4:6]),
            "hour":        int(value[6:8]),
            "minute":      int(value[8:10]),
            "record_type": value[10:12],
            "data_field":  value[12:18]
        })
        

    return data

def function_11A(tls: tlsSocket) -> dict:
    """
    Runs function 11A on a given Veeder-Root TLS device and returns a dict with 
    report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.
    """

    # Execute the command and extract common values from it immediately.
    response = tls.execute("i11A00")    
    data = get_standard_values(response)

    # Store extra non-repeated info from this response.
    data["number_of_records"] = int(response[10:12])
    data["reports"] = []

    # Get values from the remaining data, split up reports.
    remaining_data = response[12:]
    expected_data_length = 20

    if len(remaining_data) < expected_data_length: 
        return data

    split_remaining_data = split_data(remaining_data, expected_data_length)

    # Get values from each tank report.
    for value in split_remaining_data:
        data["reports"].append({
            "year":         int(value[0:2]),
            "month":        int(value[2:4]),
            "day":          int(value[4:6]),
            "hour":         int(value[6:8]),
            "minute":       int(value[8:10]),
            "service_id":   value[10:16].strip(),
            "service_code": value[16:20].strip()
        })
        
    return data

def function_11B(tls: tlsSocket) -> dict:
    """
    Runs function 11B on a given Veeder-Root TLS device and returns a dict with 
    report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.
    """

    # Execute the command and extract common values from it immediately.
    response = tls.execute("i11B00")    
    data = get_standard_values(response)

    # Store extra non-repeated info from this response.
    data["service_notice_session"] = int(response[10:11])
    data["start_year"] =             int(response[11:13])
    data["start_month"] =            int(response[13:15])
    data["start_day"] =              int(response[15:17])
    data["start_hour"] =             int(response[17:19])
    data["start_minute"] =           int(response[19:21])
    data["number_of_records"] =      int(response[21:23], 16)

    data["reports"] = []

    # Get values from the remaining data, split up reports.
    remaining_data = response[23:]
    expected_data_length = 20

    if len(remaining_data) < expected_data_length: 
        return data

    split_remaining_data = split_data(remaining_data, expected_data_length)

    # Get values from each tank report.
    for value in split_remaining_data:
        data["reports"].append({
            "start_year":   int(value[0:2]),
            "start_month":  int(value[2:4]),
            "start_day":    int(value[4:6]),
            "start_hour":   int(value[6:8]),
            "start_minute": int(value[8:10]),
            "end_year":     int(value[10:12]),
            "end_month":    int(value[12:14]),
            "end_day":      int(value[14:16]),
            "end_hour":     int(value[16:18]),
            "end_minute":   int(value[18:20])
        })

    return data

def function_201(tls: tlsSocket, tank: str) -> dict:
    """
    Runs function 201 on a given Veeder-Root TLS device and returns a dict with 
    report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.

    tank - The tank number (ex. 00 for all tanks, 01 for tank one, etc).
    """

    if len(tank) != 2:
        raise ValueError("Argument 'tank' must be exactly two digits long.")

    # Execute the command and extract common values from it immediately.
    response = tls.execute("i201" + tank)    
    data = get_standard_values(response)

    data["tanks"] = []

    # Get values from the remaining data, split up tank reports.
    remaining_data = response[10:]
    print(remaining_data)
    expected_data_length = 65

    if len(remaining_data) < expected_data_length:
        return data

    split_remaining_data = split_data(remaining_data, expected_data_length)

    # Get values from each tank report.
    for value in split_remaining_data:
        data["tanks"].append({
            "tank_number":      value[0:2],
            "product_code":     value[2:3],
            "tank_status_bits": int(value[3:7]),
            "volume":           hex_to_float(value[9:17]),
            "tc_volume":        hex_to_float(value[17:25]),
            "ullage":           hex_to_float(value[25:33]),
            "height":           hex_to_float(value[33:41]),
            "water":            hex_to_float(value[41:49]),
            "temperature":      hex_to_float(value[49:57]),
            "water_volume":     hex_to_float(value[57:65])
        })
    
    return data

def function_202(tls: tlsSocket, tank: str) -> dict:
    """
    Runs function 202 on a given Veeder-Root TLS device and returns a dict with 
    report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.

    tank - The tank number (ex. 00 for all tanks, 01 for tank one, etc).
    """

    if len(tank) != 2:
        raise ValueError("Argument 'tank' must be exactly two digits long.")

    # Execute the command and extract common values from it immediately.
    response = tls.execute("i202" + tank)    
    data = get_standard_values(response)

    data["tanks"] = []

    # Get values from the remaining data, split up tank reports.
    remaining_data = response[10:]

    # Get values from each tank report.
    while remaining_data:
        if len(remaining_data) < 107: break

        # Collecting all necessary non-repeated values.
        delivery_count = int(remaining_data[3:5])

        tank = {
            "tank_number":  remaining_data[0:2],
            "product_code": remaining_data[2:3],
            "deliveries":   []
        }

        # Slicing off the previously collected values, now getting all deliveries.
        remaining_data = remaining_data[5:]

        for _ in range(0, delivery_count):
            if len(remaining_data) < 100: break

            tank["deliveries"].append({
                "start_year":           int(remaining_data[0:2]),
                "start_month":          int(remaining_data[2:4]),
                "start_day":            int(remaining_data[4:6]),
                "start_hour":           int(remaining_data[6:8]),
                "start_minute":         int(remaining_data[8:10]),
                "end_year":             int(remaining_data[10:12]),
                "end_month":            int(remaining_data[12:14]),
                "end_day":              int(remaining_data[14:16]),
                "end_hour":             int(remaining_data[16:18]),
                "end_minute":           int(remaining_data[18:20]),
                "starting_volume":      hex_to_float(remaining_data[22:30]),
                "starting_tc_volume":   hex_to_float(remaining_data[30:38]),
                "starting_water":       hex_to_float(remaining_data[38:46]),
                "starting_temp":        hex_to_float(remaining_data[46:54]),
                "ending_volume":        hex_to_float(remaining_data[54:62]),
                "ending_tc_volume":     hex_to_float(remaining_data[62:70]),
                "ending_water":         hex_to_float(remaining_data[70:78]),
                "ending_temp":          hex_to_float(remaining_data[78:86]),
                "starting_height":      hex_to_float(remaining_data[86:94]),
                "ending_height":        hex_to_float(remaining_data[94:102])
            })

            remaining_data = remaining_data[102:]
        
        data["tanks"].append(tank)

    return data

def function_203(tls: tlsSocket, tank: str) -> dict:
    """
    Runs function 203 on a given Veeder-Root TLS device and returns a dict with 
    report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.

    tank - The tank number (ex. 00 for all tanks, 01 for tank one, etc).
    """

    if len(tank) != 2:
        raise ValueError("Argument 'tank' must be exactly two digits long.")

    # Execute the command and extract common values from it immediately.
    response = tls.execute("i203" + tank)    
    data = get_standard_values(response)

    data["tanks"] = []

    # Get values from the remaining data, split up tank reports.
    remaining_data = response[10:]
    expected_data_length = 57

    if len(remaining_data) < expected_data_length:
        return data

    split_remaining_data = split_data(remaining_data, expected_data_length)

    # Get values from each tank report.
    for value in split_remaining_data:
        data["tanks"].append({
            "tank_number":     value[0:2],
            "product_code":    value[2:3],
            "start_year":      int(value[3:5]),
            "start_month":     int(value[5:7]),
            "start_day":       int(value[7:9]),
            "start_hour":      int(value[9:11]),
            "start_minute":    int(value[11:13]),
            "test_duration":   int(value[13:15]),

            # TO-DO: Make this function check if these values are actually present 
            # based on the data fields count provided by command output.
            # This will likely cause issues if the system monitors more than three tanks, 
            # as 17*4 = 68 which exceeds the remaining data length check.
            "starting_temp":   hex_to_float(value[17:25]),
            "ending_temp":     hex_to_float(value[25:33]),
            "starting_volume": hex_to_float(value[33:41]),
            "ending_rate":     hex_to_float(value[41:49]),
            "hourly_changes":  hex_to_float(value[49:57])
        })

    return data

def function_204(tls: tlsSocket, tank: str) -> dict:
    """
    Runs function 204 on a given Veeder-Root TLS device and returns a dict with 
    report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.

    tank - The tank number (ex. 00 for all tanks, 01 for tank one, etc).
    """

    if len(tank) != 2:
        raise ValueError("Argument 'tank' must be exactly two digits long.")

    # Execute the command and extract common values from it immediately.
    response = tls.execute("i204" + tank)    
    data = get_standard_values(response)

    data["inventory"] = []

    # Get values from the remaining data, split up the inventory.
    remaining_data = response[10:]
    expected_data_length = 111

    if len(remaining_data) < expected_data_length:
        return data

    split_remaining_data = split_data(remaining_data, expected_data_length)

    # Get values from each inventory log.
    for value in split_remaining_data:
        data["inventory"].append({
            "tank_number":       value[0:2],
            "product_code":      value[2:3],
            "shift_number":      value[3:5],
            "start_volume":      hex_to_float(value[7:15]),
            "start_ullage":      hex_to_float(value[15:23]),
            "start_tc_volume":   hex_to_float(value[23:31]),
            "start_height":      hex_to_float(value[31:39]),
            "start_water":       hex_to_float(value[39:47]),
            "start_temperature": hex_to_float(value[47:55]),
            "end_volume":        hex_to_float(value[55:63]),
            "end_ullage":        hex_to_float(value[63:71]),
            "end_tc_volume":     hex_to_float(value[71:79]),
            "end_height":        hex_to_float(value[79:87]),
            "end_water":         hex_to_float(value[87:95]),
            "end_temperature":   hex_to_float(value[95:103]),
            "total_value":       hex_to_float(value[103:111])
        })

    return data

def function_205(tls: tlsSocket, tank: str) -> dict:
    """
    Runs function 205 on a given Veeder-Root TLS device and returns a dict with 
    report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.

    tank - The tank number (ex. 00 for all tanks, 01 for tank one, etc).
    """

    if len(tank) != 2:
        raise ValueError("Argument 'tank' must be exactly two digits long.")

    # Execute the command and extract common values from it immediately.
    response = tls.execute("i205" + tank)    
    data = get_standard_values(response)

    data["alarms"] = []

    # Get values from the remaining data, split up alarms.
    remaining_data = response[10:]
    expected_data_length = 6

    if len(remaining_data) < expected_data_length:
        return data

    split_remaining_data = split_data(remaining_data, expected_data_length)

    # Get values from each alarm.
    for value in split_remaining_data:
        data["alarms"].append({
            "tank_number":      value[0:2],
            "number_of_alarms": int(value[2:4]),
            "alarm_type":       int(value[4:6])
        })

    return data

def function_206(tls: tlsSocket, tank: str) -> dict:
    """
    Runs function 206 on a given Veeder-Root TLS device and returns a dict with 
    report info.

    tls - A socket for a TLS device, should be created with the tlsSocket class.

    tank - The tank number (ex. 00 for all tanks, 01 for tank one, etc).
    """

    if len(tank) != 2:
        raise ValueError("Argument 'tank' must be exactly two digits long.")

    # Execute the command and extract common values from it immediately.
    response = tls.execute("i206" + tank)    
    data = get_standard_values(response)

    data["tanks"] = {}

    # Get the list of alarms for each tank after finding how many alarms each tank has.
    remaining_data = response[10:]

    while remaining_data:
        if len(remaining_data) < 18: break

        # Collect tank number and alarm count, then slice them out of the current data.
        tank_number = remaining_data[0:2]
        alarm_count = int(remaining_data[2:4])

        remaining_data = remaining_data[4:]

        # Create a dictionary for the tank and add the alarms into an associated list.
        data["tanks"][tank_number] = []
    
        for _ in range(0, alarm_count):
            if len(remaining_data) < 14: break
            
            data["tanks"][tank_number].append({
                "year":       int(remaining_data[0:2]),
                "month":      int(remaining_data[2:4]),
                "day":        int(remaining_data[4:6]),
                "hour":       int(remaining_data[6:8]),
                "minute":     int(remaining_data[8:10]),
                "alarm_type": remaining_data[10:14]
            })

            # Slice off values that have already been added.
            remaining_data = remaining_data[14:]

    return data
