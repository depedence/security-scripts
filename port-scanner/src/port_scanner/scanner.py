import socket
import sys


def is_open(host, port) -> bool:
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except OSError:
        return False


def main():
    if len(sys.argv) < 4:
        print("Usage: python scanner.py <host> <start_port> <end_port>")
        sys.exit(1)

    results = {}
    host = sys.argv[1]
    try:
        start_port = int(sys.argv[2])
        end_port = int(sys.argv[3])
    except ValueError:
        print("Ports must be numbers")
        sys.exit(1)
    if start_port > end_port:
        print("Start port must not be greater than end port")
        sys.exit(1)

    print(f"Scanning {host} ports {start_port}-{end_port}")

    for port in range(start_port, end_port + 1):
        if is_open(host, port):
            results[port] = "open"

    for port, result in results.items():
        print(f"{port}: {result}")
    print(f"Done: {len(results)} open")


if __name__ == "__main__":
    main()
