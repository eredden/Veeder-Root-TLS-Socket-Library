# tls_client.py - A command-line interface for communicating with TLS automatic tank gauges.

from veeder_root_tls_socket_library.socket import TlsSocket
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="IP address of the TLS system.", type=str)
    parser.add_argument("port", help="Port number used to connect to the" \
        "serial interface remotely.", type=int)
    args = parser.parse_args()

    with TlsSocket(args.ip, args.port) as tls:
        print(f"You are connected to {args.ip} using port {args.port}.")

        while True:
            command = input("\n>> ").lower()

            match command:
                case "help":
                    print("Veeder-Root tank gauge commands can be found in the Serial Interface" \
                        " manual for that model of tank gauge.")
                    print("You can exit this program by using the 'exit' command at any time.")

                case "exit": 
                    break

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