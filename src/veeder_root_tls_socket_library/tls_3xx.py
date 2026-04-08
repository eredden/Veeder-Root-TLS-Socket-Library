# tls_3xx.py - A series of functions used to extract data from TLS system outputs.

from veeder_root_tls_socket_library.format import _get_timestamp, _split_data, _hex_to_float

def function_101(response: str) -> dict:
    """
    Parses function 101 output from a Veeder-Root TLS device and returns a dict 
    with report info.

    response - The byte response from the function converted to a string format.
    """

    if not type(response) == str: 
        raise ValueError("Argument 'response' must be a string.")

    # Execute the command and extract common values from it immediately.
    data = _get_timestamp(response)
    
    data["alarms"] = []

    # Get values from the remaining data, split up alarms.
    response = response[10:]
    data_length = 6

    # Get values from each alarm.
    if len(response) >= data_length: 
        for value in _split_data(response, data_length):
            data["alarms"].append({
                "alarm_category": int(value[0:2]),
                "alarm_type":     int(value[2:4]),
                "tank_number":    value[4:6]
            })

    return data
        
def function_102(response: str) -> dict:
    """
    Parses function 102 output from a Veeder-Root TLS device and returns a dict 
    with report info.

    response - The byte response from the function converted to a string format.
    """

    if not type(response) == str: 
        raise ValueError("Argument 'response' must be a string.")

    # Execute the command and extract common values from it immediately.  
    data = _get_timestamp(response)
    
    data["slots"] = []

    # Get values from the remaining data, split up slots.
    response = response[12:]
    data_length = 20

    # Get values from each slot.
    if len(response) >= data_length: 
        for value in _split_data(response, data_length):
            data["slots"].append({
                "slot_number":        int(value[0:2], 16),
                "type_of_module":     value[2:4],
                "power_on_reset":     _hex_to_float(value[4:12]),
                "current_io_reading": _hex_to_float(value[12:19])
            })

    return data

def function_111(response: str) -> dict:
    """
    Parses function 111 output from a Veeder-Root TLS device and returns a dict 
    with report info.

    response - The byte response from the function converted to a string format.
    """

    if not type(response) == str:
        raise ValueError("Argument 'response' must be a string.")

    # Execute the command and extract common values from it immediately.
    data = _get_timestamp(response)
    
    data["alarms"] = []

    # Get values from the remaining data, split up alarms.
    response = response[10:]
    data_length = 20

    # Get values from each alarm.
    if len(response) >= data_length:
        for value in _split_data(response, data_length):
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

def function_112(response: str) -> dict:
    """
    Parses function 112 output from a Veeder-Root TLS device and returns a dict 
    with report info.

    response - The byte response from the function converted to a string format.
    """

    if not type(response) == str: 
        raise ValueError("Argument 'response' must be a string.")

    # Execute the command and extract common values from it immediately.
    data = _get_timestamp(response)
    
    data["alarms"] = []

    # Get values from the remaining data, split up alarms.
    response = response[10:]
    data_length = 20

    # Get values from each alarm.
    if len(response) >= data_length: 
        for value in _split_data(response, data_length):
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

def function_113(response: str) -> dict:
    """
    Parses function 113 output from a Veeder-Root TLS device and returns a dict 
    with report info.

    response - The byte response from the function converted to a string format.
    """

    if not type(response) == str: 
        raise ValueError("Argument 'response' must be a string.")

    # Execute the command and extract common values from it immediately.
    data = _get_timestamp(response)

    # Store extra non-repeated info from this response.
    data["station_header_1"] = response[10:30].strip()
    data["station_header_2"] = response[30:50].strip()
    data["station_header_3"] = response[50:70].strip()
    data["station_header_4"] = response[70:90].strip()
    
    data["alarms"] = []

    # Get values from the remaining data, split up alarms.
    response = response[90:]
    data_length = 18

    # Get values from each alarm.
    if len(response) >= data_length: 
        for value in _split_data(response, data_length):
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

def function_114(response: str) -> dict:
    """
    Parses function 114 output from a Veeder-Root TLS device and returns a dict 
    with report info.

    response - The byte response from the function converted to a string format.
    """

    if not type(response) == str: 
        raise ValueError("Argument 'response' must be a string.")

    # Execute the command and extract common values from it immediately.
    data = _get_timestamp(response)

    # Store extra non-repeated info from this response.
    data["station_header_1"] = response[10:30].strip()
    data["station_header_2"] = response[30:50].strip()
    data["station_header_3"] = response[50:70].strip()
    data["station_header_4"] = response[70:90].strip()
    
    data["alarms"] = []

    # Get values from the remaining data, split up alarms.
    response = response[90:]
    data_length = 20

    # Get values from each alarm.
    if len(response) >= data_length: 
        for value in _split_data(response, data_length):
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

def function_115(response: str) -> dict:
    """
    Parses function 115 output from a Veeder-Root TLS device and returns a dict 
    with report info.

    response - The byte response from the function converted to a string format.
    """

    if not type(response) == str: 
        raise ValueError("Argument 'response' must be a string.")

    # Execute the command and extract common values from it immediately.
    data = _get_timestamp(response)

    # Store extra non-repeated info from this response.
    data["station_header_1"] = response[10:30].strip()
    data["station_header_2"] = response[30:50].strip()
    data["station_header_3"] = response[50:70].strip()
    data["station_header_4"] = response[70:90].strip()

    data["alarms"] = []

    # Get values from the remaining data, split up alarms.
    response = response[90:]
    data_length = 18

    # Get values from each alarm.
    if len(response) >= data_length: 
        for value in _split_data(response, data_length):
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

def function_116(response: str) -> dict:
    """
    Parses function 116 output from a Veeder-Root TLS device and returns a dict 
    with report info.

    response - The byte response from the function converted to a string format.
    """

    if not type(response) == str: 
        raise ValueError("Argument 'response' must be a string.")

    # Execute the command and extract common values from it immediately.
    data = _get_timestamp(response)

    # Store extra non-repeated info from this response.
    data["station_header_1"] =  response[10:30].strip()
    data["station_header_2"] =  response[30:50].strip()
    data["station_header_3"] =  response[50:70].strip()
    data["station_header_4"] =  response[70:90].strip()
    data["number_of_records"] = int(response[90:92])

    data["reports"] = []

    # Get values from the remaining data, split up reports.
    response = response[90:]
    data_length = 25
    
    # Get values from each report.
    if len(response) >= data_length: 
        for value in _split_data(response, data_length):
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

def function_119(response: str) -> dict:
    """
    Parses function 119 output from a Veeder-Root TLS device and returns a dict 
    with report info.

    response - The byte response from the function converted to a string format.
    """

    if not type(response) == str: 
        raise ValueError("Argument 'response' must be a string.")

    # Execute the command and extract common values from it immediately.
    data = _get_timestamp(response)

    # Store extra non-repeated info from this response.
    data["number_of_records"] = int(response[10:14])
    data["records"] = []

    # Get values from the remaining data, split up records.
    response = response[14:]
    data_length = 18

    # Get values from each record.
    if len(response) >= data_length: 
        for value in _split_data(response, data_length):
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

def function_11A(response: str) -> dict:
    """
    Parses function 11A output from a Veeder-Root TLS device and returns a dict 
    with report info.

    response - The byte response from the function converted to a string format.
    """

    if not type(response) == str:
        raise ValueError("Argument 'response' must be a string.")

    # Execute the command and extract common values from it immediately.
    data = _get_timestamp(response)

    # Store extra non-repeated info from this response.
    data["number_of_records"] = int(response[10:12])
    data["reports"] = []

    # Get values from the remaining data, split up reports.
    response = response[12:]
    data_length = 20

    # Get values from each tank report.
    if len(response) >= data_length: 
        for value in _split_data(response, data_length):
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

def function_11B(response: str) -> dict:
    """
    Parses function 11B output from a Veeder-Root TLS device and returns a dict 
    with report info.

    response - The byte response from the function converted to a string format.
    """

    if not type(response) == str: 
        raise ValueError("Argument 'response' must be a string.")

    # Execute the command and extract common values from it immediately.
    data = _get_timestamp(response)

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
    response = response[23:]
    data_length = 20

    # Get values from each tank report.
    if len(response) >= data_length: 
        for value in _split_data(response, data_length):
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

def function_201(response: str) -> dict:
    """
    Parses function 201 output from a Veeder-Root TLS device and returns a dict 
    with report info.

    response - The byte response from the function converted to a string format.
    """

    if not type(response) == str: 
        raise ValueError("Argument 'response' must be a string.")

    # Execute the command and extract common values from it immediately.
    data = _get_timestamp(response)

    data["tanks"] = []

    # Get values from the remaining data, split up tank reports.
    response = response[10:]
    data_length = 65

    # Get values from each tank report.
    if len(response) >= data_length:
        for value in _split_data(response, data_length):
            data["tanks"].append({
                "tank_number":      value[0:2],
                "product_code":     value[2:3],
                "tank_status_bits": int(value[3:7], 16),
                "volume":           _hex_to_float(value[9:17]),
                "tc_volume":        _hex_to_float(value[17:25]),
                "ullage":           _hex_to_float(value[25:33]),
                "height":           _hex_to_float(value[33:41]),
                "water":            _hex_to_float(value[41:49]),
                "temperature":      _hex_to_float(value[49:57]),
                "water_volume":     _hex_to_float(value[57:65])
            })
    
    return data

def function_202(response: str) -> dict:
    """
    Parses function 202 output from a Veeder-Root TLS device and returns a dict 
    with report info.

    response - The byte response from the function converted to a string format.
    """

    if not type(response) == str: 
        raise ValueError("Argument 'response' must be a string.")

    # Execute the command and extract common values from it immediately.
    data = _get_timestamp(response)

    data["tanks"] = []

    # Get values from the remaining data, split up tank reports.
    response = response[10:]

    # Get values from each tank report.
    while response:
        if len(response) < 107: break

        # Collecting all necessary non-repeated values.
        delivery_count = int(response[3:5])

        tank = {
            "tank_number":  response[0:2],
            "product_code": response[2:3],
            "deliveries":   []
        }

        # Slicing off previously collected values, now getting all deliveries.
        response = response[5:]

        for _ in range(0, delivery_count):
            if len(response) < 100: break

            tank["deliveries"].append({
                "start_year":           int(response[0:2]),
                "start_month":          int(response[2:4]),
                "start_day":            int(response[4:6]),
                "start_hour":           int(response[6:8]),
                "start_minute":         int(response[8:10]),
                "end_year":             int(response[10:12]),
                "end_month":            int(response[12:14]),
                "end_day":              int(response[14:16]),
                "end_hour":             int(response[16:18]),
                "end_minute":           int(response[18:20]),
                "starting_volume":      _hex_to_float(response[22:30]),
                "starting_tc_volume":   _hex_to_float(response[30:38]),
                "starting_water":       _hex_to_float(response[38:46]),
                "starting_temp":        _hex_to_float(response[46:54]),
                "ending_volume":        _hex_to_float(response[54:62]),
                "ending_tc_volume":     _hex_to_float(response[62:70]),
                "ending_water":         _hex_to_float(response[70:78]),
                "ending_temp":          _hex_to_float(response[78:86]),
                "starting_height":      _hex_to_float(response[86:94]),
                "ending_height":        _hex_to_float(response[94:102])
            })

            response = response[102:]
        
        data["tanks"].append(tank)

    return data

def function_203(response: str) -> dict:
    """
    Parses function 203 output from a Veeder-Root TLS device and returns a dict 
    with report info.

    response - The byte response from the function converted to a string format.
    """

    if not type(response) == str: 
        raise ValueError("Argument 'response' must be a string.")

    # Execute the command and extract common values from it immediately.
    data = _get_timestamp(response)

    data["tanks"] = []

    # Get values from the remaining data, split up tank reports.
    response = response[10:]
    data_length = 57

    # Get values from each tank report.
    if len(response) >= data_length:
        for value in _split_data(response, data_length):
            data["tanks"].append({
                "tank_number":     value[0:2],
                "product_code":    value[2:3],
                "start_year":      int(value[3:5]),
                "start_month":     int(value[5:7]),
                "start_day":       int(value[7:9]),
                "start_hour":      int(value[9:11]),
                "start_minute":    int(value[11:13]),
                "test_duration":   int(value[13:15]),
                "starting_temp":   _hex_to_float(value[17:25]),
                "ending_temp":     _hex_to_float(value[25:33]),
                "starting_volume": _hex_to_float(value[33:41]),
                "ending_rate":     _hex_to_float(value[41:49]),
                "hourly_changes":  _hex_to_float(value[49:57])
            })

    return data

def function_204(response: str) -> dict:
    """
    Parses function 204 output from a Veeder-Root TLS device and returns a dict 
    with report info.

    response - The byte response from the function converted to a string format.
    """

    if not type(response) == str: 
        raise ValueError("Argument 'response' must be a string.")

    # Execute the command and extract common values from it immediately.    
    data = _get_timestamp(response)

    data["inventory"] = []

    # Get values from the remaining data, split up the inventory.
    response = response[10:]
    data_length = 111

    # Get values from each inventory log.
    if len(response) >= data_length:
        for value in _split_data(response, data_length):
            data["inventory"].append({
                "tank_number":       value[0:2],
                "product_code":      value[2:3],
                "shift_number":      value[3:5],
                "start_volume":      _hex_to_float(value[7:15]),
                "start_ullage":      _hex_to_float(value[15:23]),
                "start_tc_volume":   _hex_to_float(value[23:31]),
                "start_height":      _hex_to_float(value[31:39]),
                "start_water":       _hex_to_float(value[39:47]),
                "start_temperature": _hex_to_float(value[47:55]),
                "end_volume":        _hex_to_float(value[55:63]),
                "end_ullage":        _hex_to_float(value[63:71]),
                "end_tc_volume":     _hex_to_float(value[71:79]),
                "end_height":        _hex_to_float(value[79:87]),
                "end_water":         _hex_to_float(value[87:95]),
                "end_temperature":   _hex_to_float(value[95:103]),
                "total_value":       _hex_to_float(value[103:111])
            })

    return data

def function_205(response: str) -> dict:
    """
    Parses function 205 output from a Veeder-Root TLS device and returns a dict 
    with report info.

    response - The byte response from the function converted to a string format.
    """

    if not type(response) == str: 
        raise ValueError("Argument 'response' must be a string.")

    # Execute the command and extract common values from it immediately.
    data = _get_timestamp(response)

    data["alarms"] = []

    # Get values from the remaining data, split up alarms.
    response = response[10:]

    while len(response) > 0:
        number_of_alarms = int(response[2:4], 16)

        if number_of_alarms > 0:
            data["alarms"].append({
                "tank_number":      response[0:2],
                "number_of_alarms": number_of_alarms,
                "alarm_type":       response[4:6]
            })

            response = response[6:]
        else:
            data["alarms"].append({
                "tank_number":      response[0:2],
                "number_of_alarms": number_of_alarms
            })

            response = response[4:]

    return data

def function_206(response: str) -> dict:
    """
    Parses function 206 output from a Veeder-Root TLS device and returns a dict 
    with report info.

    response - The byte response from the function converted to a string format.
    """

    if not type(response) == str: 
        raise ValueError("Argument 'response' must be a string.")

    # Execute the command and extract common values from it immediately.
    data = _get_timestamp(response)

    data["tanks"] = {}

    # Get the list of alarms for each tank after finding alarm per tank count.
    response = response[10:]

    while response:
        if len(response) < 18: break

        # Collect tank number and alarm count, then slice them out of the data.
        tank_number = response[0:2]
        alarm_count = int(response[2:4])

        response = response[4:]

        # Create a dictionary for the tank and add the alarms into a list.
        data["tanks"][tank_number] = []
    
        for _ in range(0, alarm_count):
            if len(response) < 14: break
            
            data["tanks"][tank_number].append({
                "year":       int(response[0:2]),
                "month":      int(response[2:4]),
                "day":        int(response[4:6]),
                "hour":       int(response[6:8]),
                "minute":     int(response[8:10]),
                "alarm_type": response[10:14]
            })

            # Slice off values that have already been added.
            response = response[14:]

    return data

def function_207(response: str) -> dict:
    """
    Parses function 207 output from a Veeder-Root TLS device and returns a dict 
    with report info.

    response - The byte response from the function converted to a string format.
    """

    if not type(response) == str: 
        raise ValueError("Argument 'response' must be a string.")

    # Execute the command and extract common values from it immediately.
    data = _get_timestamp(response)

    data["tanks"] = {}

    # Get the list of tests for each tank after finding test per tank count.
    response = response[10:]

    while response:
        if len(response) < 44: break

        # Collect tank number and test count, then slice them out.
        tank_number = response[0:2]
        test_count = int(response[2:4], 16)

        response = response[4:]

        # Create a dictionary for the tank and add the tests into an list.
        data["tanks"][tank_number] = []
    
        for _ in range(0, test_count):
            if len(response) < 40: break
            
            data["tanks"][tank_number].append({
                "report_type":         response[0:2],
                "leak_history_number": response[2:4],
                "test_type":           response[4:6],
                "year":                int(response[6:8]),
                "month":               int(response[8:10]),
                "day":                 int(response[10:12]),
                "hour":                int(response[12:14]),
                "minute":              int(response[14:16]),
                "duration":            _hex_to_float(response[16:24]),
                "volume":              _hex_to_float(response[24:32]),
                "volume_percentage":   _hex_to_float(response[32:40])
            })

            # Slice off values that have already been added.
            response = response[40:]

    return data

def function_208(response: str) -> dict:
    """
    Parses function 208 output from a Veeder-Root TLS device and returns a 
    with report info.

    response - The byte response from the function converted to a string format.
    """

    if not type(response) == str: 
        raise ValueError("Argument 'response' must be a string.")

    # Execute the command and extract common values from it immediately.
    data = _get_timestamp(response)

    data["tanks"] = {}

    # Get the list of tests for each tank after finding test per tank count.
    response = response[10:]

    while response:
        if len(response) < 44: break

        # Collect tank number and test count, then slice them out.
        tank_number = response[0:2]
        test_count = int(response[2:4], 16)

        response = response[4:]

        # Create a dictionary for the tank and add the tests into an list.
        data["tanks"][tank_number] = []
    
        for _ in range(0, test_count):
            if len(response) < 40: break
            
            data["tanks"][tank_number].append({
                "test_result_type":     response[0:2],
                "test_manifold_status": response[2:4],
                "year":                 int(response[4:6]),
                "month":                int(response[6:8]),
                "day":                  int(response[8:10]),
                "hour":                 int(response[10:12]),
                "minute":               int(response[12:14]),
                "test_result":          response[14:16],
                "test_rate":            _hex_to_float(response[16:24]),
                "duration":             _hex_to_float(response[24:32]),
                "volume":               _hex_to_float(response[32:40])
            })

            # Slice off values that have already been added.
            response = response[40:]

    return data

# Functions 20A through 219 need to be added.

def function_21A(response: str) -> dict:
    """
    Parses function 21A output from a Veeder-Root TLS device and returns a dict 
    with report info.

    response - The byte response from the function converted to a string format.
    """

    if not type(response) == str: 
        raise ValueError("Argument 'response' must be a string.")

    # Execute the command and extract common values from it immediately.
    data = _get_timestamp(response)

    data["tanks"] = []

    # Get values from the remaining data, split up tank reports.
    response = response[10:]
    data_length = 65

    # Get values from each tank report.
    if len(response) >= data_length:
        for value in _split_data(response, data_length):
            data["tanks"].append({
                "tank_number":      value[0:2],
                "product_code":     value[2:3],
                "tank_status_bits": int(value[3:7], 16),
                "volume":           _hex_to_float(value[9:17]),
                "tc_volume":        _hex_to_float(value[17:25]),
                "ullage":           _hex_to_float(value[25:33]),
                "height":           _hex_to_float(value[33:41]),
                "water":            _hex_to_float(value[41:49]),
                "temperature":      _hex_to_float(value[49:57]),
                "water_volume":     _hex_to_float(value[57:65])
            })
    
    return data

# The TLS system I am using does not support this function. This is untested.
def function_21B(response: str) -> dict:
    """
    Parses function 21B output from a Veeder-Root TLS device and returns a dict 
    with report info.

    response - The byte response from the function converted to a string format.
    """

    if not type(response) == str: 
        raise ValueError("Argument 'response' must be a string.")

    # Execute the command and extract common values from it immediately.
    data = _get_timestamp(response)

    data["tanks"] = {}

    # Get the list of deliveries for each tank.
    response = response[10:]

    while response:
        if len(response) < 194: break

        # Collect tank number and delivery count, then slice them out.
        tank_number = response[0:2]
        delivery_count = int(response[2:4])

        response = response[4:]

        # Create a dictionary for the tank and add the deliveries into an list.
        data["tanks"][tank_number] = []
    
        for _ in range(0, delivery_count):
            if len(response) < 190: break
            
            data["tanks"][tank_number].append({
                "start_year":                                       int(response[0:2]),
                "start_month":                                      int(response[2:4]),
                "start_day":                                        int(response[4:6]),
                "start_hour":                                       int(response[6:8]),
                "start_minute":                                     int(response[8:10]),
                "end_year":                                         int(response[10:12]),
                "end_month":                                        int(response[12:14]),
                "end_day":                                          int(response[14:16]),
                "end_hour":                                         int(response[16:18]),
                "end_minute":                                       int(response[18:20]),
                "start_volume":                                     _hex_to_float(response[22:30]),
                "end_volume":                                       _hex_to_float(response[30:38]),
                "adjusted_delivery_volume":                         _hex_to_float(response[38:46]),
                "adjusted_temperature_compensated_delivery_volume": _hex_to_float(response[46:54]),
                "start_fuel_height":                                _hex_to_float(response[54:62]),
                "start_fuel_temperature_1":                         _hex_to_float(response[62:70]),
                "start_fuel_temperature_2":                         _hex_to_float(response[70:78]),
                "start_fuel_temperature_3":                         _hex_to_float(response[78:86]),
                "start_fuel_temperature_4":                         _hex_to_float(response[86:94]),
                "start_fuel_temperature_5":                         _hex_to_float(response[94:102]),
                "start_fuel_temperature_6":                         _hex_to_float(response[102:110]),
                "end_fuel_height":                                  _hex_to_float(response[110:118]),
                "end_fuel_temperature_1":                           _hex_to_float(response[118:126]),
                "end_fuel_temperature_2":                           _hex_to_float(response[126:134]),
                "end_fuel_temperature_3":                           _hex_to_float(response[134:142]),
                "end_fuel_temperature_4":                           _hex_to_float(response[142:150]),
                "end_fuel_temperature_5":                           _hex_to_float(response[150:158]),
                "end_fuel_temperature_6":                           _hex_to_float(response[158:166]),
                "total_dispensed":                                  _hex_to_float(response[166:174]),
                "start_fuel_temperature_average":                   _hex_to_float(response[174:182]),
                "end_fuel_temperature average":                     _hex_to_float(response[182:190])
            })

            # Slice off values that have already been added.
            response = response[190:]

    return data

def function_221(response: str) -> dict:
    """
    Parses function 221 output from a Veeder-Root TLS device and returns a dict 
    with report info.

    response - The byte response from the function converted to a string format.
    """

    if not type(response) == str: 
        raise ValueError("Argument 'response' must be a string.")

    # Execute the command and extract common values from it immediately.
    data = _get_timestamp(response)

    data["reports"] = []

    # Get values from the remaining data, split up reports.
    response = response[10:]

    while response:
        if len(response) < 68: break

        # Collect tank number and alarm count, then slice them out.
        tank_number    = response[0:2]
        product_code   = response[2:3]
        probe_type     = response[3:5]
        delivery_count = int(response[5:8])

        response = response[8:]

        # Create a dictionary for the tank and add the alarms into an list.
        data["reports"][tank_number] = []
    
        for _ in range(0, delivery_count):
            if len(response) < 60: break
            
            data["tanks"][tank_number].append({
                "product_code":                   product_code,
                "probe_type":                     probe_type,
                "year":                           int(response[0:2]),
                "month":                          int(response[2:4]),
                "day":                            int(response[4:6]),
                "hour":                           int(response[6:8]),
                "minute":                         int(response[8:10]),
                "ticket_volume":                  _hex_to_float(response[12:20]),
                "gauged_volume":                  _hex_to_float(response[20:28]),
                "delivery_variance":              _hex_to_float(response[28:36]),
                "start_fuel_temperature":         _hex_to_float(response[36:44]),
                "end_fuel_temperature":           _hex_to_float(response[44:52]),
                "estimated_delivery_temperature": _hex_to_float(response[52:60])
            })

            # Slice off values that have already been added.
            response = response[60:]

    return data


# Functions 222 through 227 need to be added.

def function_251(response: str) -> dict:
    """
    Parses function 251 output from a Veeder-Root TLS device and returns a dict 
    with report info.

    response - The byte response from the function converted to a string format.
    """

    if not type(response) == str: 
        raise ValueError("Argument 'response' must be a string.")

    # Execute the command and extract common values from it immediately.
    data = _get_timestamp(response)
    
    data["reports"] = []

    # Get values from the remaining data, split up reports.
    response = response[10:]
    data_length = 4

    # Get values from each alarm.
    if len(response) >= data_length: 
        for value in _split_data(response, data_length):
            data["reports"].append({
                "tank_number":  value[0:2],
                "csld_results": value[2:4] 
            })

    return data

def function_602(response: str) -> dict:
    """
    Parses function 602 output from a Veeder-Root TLS device and returns a dict 
    with report info.

    response - The byte response from the function converted to a string format.
    """

    if not type(response) == str: 
        raise ValueError("Argument 'response' must be a string.")

    # Execute the command and extract common values from it immediately.
    data = _get_timestamp(response)
    
    data["labels"] = {}

    # Get values from the remaining data, split up labels.
    response = response[10:]
    data_length = 22

    # Get values from each alarm.
    if len(response) >= data_length: 
        for value in _split_data(response, data_length):
            tank_number = int(value[0:2])
            label = str(value[2:23]).strip()

            data["labels"][tank_number] = label

    return data