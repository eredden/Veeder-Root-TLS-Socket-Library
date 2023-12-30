import tls_socket
import argparse

def is_security_code_valid(security_code: str) -> bool:

    """
    Checks if the user-provided RS-232 security code meets length and character requirements.

    security_code - Contains the security code provided by the user.
    """

    # If a security code was not provided, simply return true.
    if security_code == None:
        return True

    # Check if security code uses ASCII characters.
    try:
        security_code.encode('ascii')
    except:
        return False
    
    # Ensure that security code length is six characters.
    if len(security_code) != 6:
        return False
    
    return True


if __name__ == "__main__":
    # Require IP address and port parameters when running this script.
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="IP address of the TLS system.", type=str)
    parser.add_argument("port", help="Port number used to connect to the serial interface remotely.", type=int)
    parser.add_argument("--security_code", help="Six printable-character ASCII code prepended to commands for authentication.", type=str)
    args = parser.parse_args()

    # Check if security code meets proper standards.
    if not is_security_code_valid(args.security_code):
        print("The security code must use ASCII characters and be six characters in length.")
        raise ValueError
    elif args.security_code == None:
        args.security_code = ""

    # Start a connection with the desired host.
    with tls_socket.tlsSocket(args.ip, args.port) as tls:
        
        print(f"You are connected to {args.ip} using port {args.port}.\n")

        while True:
            command = input(">> ")

            command = bytes(f"{args.security_code}{command}", "utf-8")
            results = tls.execute(command, 5, True)
