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

            if command.lower() == "exit":
                print("Disconnecting from host...")
                break

            if command == "":
                continue

            try:
                output = tls.execute(command)
                print(output)
            except ValueError as err:
                print(err.args[0])

        print("Connection ended.\n")
