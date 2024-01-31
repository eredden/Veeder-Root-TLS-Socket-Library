import tls_socket
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="IP address of the TLS system.", type=str)
    parser.add_argument("port", help="Port number used to connect to the \
                        serial interface remotely.", type=int)
    parser.add_argument("--timeout", help="Sets the delay in seconds between \
                        sending a command and storing output.", 
                        nargs='?', default=1, type=int)
    args = parser.parse_args()

    with tls_socket.tlsSocket(args.ip, args.port) as tls:
        print(f"You are connected to {args.ip} using port {args.port}.")

        while True:
            command = input("\n>> ")

            if command.lower() == "exit":
                print("Disconnecting from host...")
                break

            if command != "":
                output = tls.execute(command, args.timeout)
                print(output)

        print("Connection ended.\n")
