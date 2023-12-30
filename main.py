from lib import tls_socket
import argparse

if __name__ == "__main__":
    # Require IP address and port parameters when running this script.
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="IP address of the TLS system.", type=str)
    parser.add_argument("port", help="Port number used to connect to the serial interface remotely.", type=int)
    args = parser.parse_args()

    # Start a connection with the desired host.
    with tls_socket.tlsSocket(args.ip, args.port) as tls:

        print(f"You are connected to {args.ip} using port {args.port}.\n")

        # Prompt user for input FOREVER!
        while True:
            command = input(">> ")
            command = bytes(command, "utf-8")
            results = tls.execute(command, 5)

            # Converting bytecode results into a string.
            results = results.decode("utf-8")
            print(f"{results}\n")
