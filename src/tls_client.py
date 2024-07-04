# tls_client.py - A command-line interface for communicating with TLS automatic tank gauges.

import tls_socket
import tls_3xx_functions
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="IP address of the TLS system.", type=str)
    parser.add_argument("port", help="Port number used to connect to the" \
        "serial interface remotely.", type=int)
    args = parser.parse_args()

    with tls_socket.tlsSocket(args.ip, args.port) as tls:
        print(f"You are connected to {args.ip} using port {args.port}.")

        while True:
            command = input("\n>> ").lower()

            match command:
                # Function codes from tls_3xx_functions.py.
                case "101": 
                    tank = input("TANK NUMBER: ")

                    try: output = tls_3xx_functions.function_101(tls, tank)
                    except ValueError as err: output = err.args[0]

                case "102": 
                    try: output = tls_3xx_functions.function_102(tls)
                    except ValueError as err: output = err.args[0]
                    
                case "111": 
                    try: output = tls_3xx_functions.function_111(tls)
                    except ValueError as err: output = err.args[0]

                case "112": 
                    try: output = tls_3xx_functions.function_112(tls)
                    except ValueError as err: output = err.args[0]

                case "113": 
                    try: output = tls_3xx_functions.function_113(tls)
                    except ValueError as err: output = err.args[0]

                case "114": 
                    try: output = tls_3xx_functions.function_114(tls) 
                    except ValueError as err: output = err.args[0]

                case "115": 
                    try: output = tls_3xx_functions.function_115(tls)
                    except ValueError as err: output = err.args[0]

                case "116": 
                    try: output = tls_3xx_functions.function_116(tls)
                    except ValueError as err: output = err.args[0]

                case "119": 
                    start_date = input("START DATE (yymmdd): ")
                    end_date   = input("END DATE (yymmdd): ")
                    
                    try: output = tls_3xx_functions.function_119(tls, start_date, end_date)
                    except ValueError as err: output = err.args[0]

                case "11A": 
                    try: output = tls_3xx_functions.function_11A(tls)
                    except ValueError as err: output = err.args[0]

                case "11B": 
                    try: output = tls_3xx_functions.function_11B(tls)
                    except ValueError as err: output = err.args[0]

                case "201": 
                    tank = input("TANK NUMBER: ")

                    try: output = tls_3xx_functions.function_201(tls, tank)
                    except ValueError as err: output = err.args[0]

                case "202": 
                    tank = input("TANK NUMBER: ")

                    try: output = tls_3xx_functions.function_202(tls, tank)
                    except ValueError as err: output = err.args[0]

                case "203": 
                    tank = input("TANK NUMBER: ")

                    try: output = tls_3xx_functions.function_203(tls, tank)
                    except ValueError as err: output = err.args[0]

                case "204": 
                    tank = input("TANK NUMBER: ")

                    try: output = tls_3xx_functions.function_204(tls, tank)
                    except ValueError as err: output = err.args[0]

                case "205": 
                    tank = input("TANK NUMBER: ")

                    try: output = tls_3xx_functions.function_205(tls, tank)
                    except ValueError as err: output = err.args[0]

                case "206": 
                    tank = input("TANK NUMBER: ")

                    try: output = tls_3xx_functions.function_206(tls, tank)
                    except ValueError as err: output = err.args[0]

                case "207": 
                    tank = input("TANK NUMBER: ")

                    try: output = tls_3xx_functions.function_207(tls, tank)
                    except ValueError as err: output = err.args[0]

                case "208": 
                    tank = input("TANK NUMBER: ")

                    try: output = tls_3xx_functions.function_208(tls, tank)
                    except ValueError as err: output = err.args[0]

                case "21A": 
                    tank = input("TANK NUMBER: ")

                    try: output = tls_3xx_functions.function_21A(tls, tank)
                    except ValueError as err: output = err.args[0]

                case "21B": 
                    tank = input("TANK NUMBER: ")
                    deliveries = input("NUMBER OF DELIVERIES: ")

                    try: output = tls_3xx_functions.function_21B(tls, tank, deliveries)
                    except ValueError as err: output = err.args[0]

                case "251": 
                    tank = input("TANK NUMBER: ")
                    
                    try: output = tls_3xx_functions.function_251(tls, tank)
                    except ValueError as err: output = err.args[0]

                # Standard base commands.
                case "help":
                    print("Veeder-Root tank gauge commands can be found in the Serial Interface" \
                        " manual for that model of tank gauge.")
                    print("You can exit this program by using the 'exit' command at any time.")

                case "exit": break

                # Handling other inputs by simply running them against the TLS system.
                case _:
                    try:                      output = tls.execute(command)
                    except ValueError as err: output = err.args[0] 

            if type(output) == dict:
                for key in output.keys():
                    print(f"{key}: {output[key]}")
            else:
                print(output)

        print("Connection ended.\n")