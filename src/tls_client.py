import tls_socket
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
            command = input("\n>> ")

            if command.lower() == "help":
                print("Veeder-Root tank gauge commands can be found in the Serial Interface" \
                      " manual for that model of tank gauge.")
                print("You can exit this program by using the 'exit' command at any time.")
                continue
            if command.lower() == "exit": break
            if command.lower() == "":  continue

            try:                      output = tls.execute(command)
            except ValueError as err: output = err.args[0] 

            print(output)

        print("Connection ended.\n")
