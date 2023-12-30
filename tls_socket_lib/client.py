import tls_socket
import argparse

if __name__ == "__main__":

    # Require these parameters when running this script.
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="IP address of the TLS system.", type=str)
    parser.add_argument("port", help="Port number used to connect to the serial interface remotely.", type=int)
    parser.add_argument("--raw", help="Shows output from the TLS system as original, unaltered bytecode.", action="store_true")
    args = parser.parse_args()

    # Start a connection with the desired host.
    with tls_socket.tlsSocket(args.ip, args.port) as tls:
        
        print(f"You are connected to {args.ip} using port {args.port}.")

        while True:
            command = input("\n>> ")

            # If exit command is given, terminate the connection.
            if command.lower() == "exit":
                print("Disconnecting from host...")
                break

            # Run the command and save it to the output variable.
            output = tls.execute(command, 5)
            
            # Depending on whether or not the raw data was requested, output pretty or raw data.
            if args.raw == True:
                print(output)
            else:
                output = tls_socket.remove_response_headers(output, command)
                print(output)

        
        print("Connection ended.\n")
