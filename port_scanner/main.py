#!/usr/bin/env python3
"""
Port Scanner - Starter Template for Students
Assignment 2: Network Security

This is a STARTER TEMPLATE to help you get started.
You should expand and improve upon this basic implementation.

TODO for students:
1. Implement multi-threading for faster scans
2. Add banner grabbing to detect services
3. Add support for CIDR notation (e.g., 192.168.1.0/24)
4. Add different scan types (SYN scan, UDP scan, etc.)
5. Add output formatting (JSON, CSV, etc.)
6. Implement timeout and error handling
7. Add progress indicators
8. Add service fingerprinting
"""

import socket
import sys
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed


def scan_port(target, port, timeout=1.0):
    """
    Scan a single port on the target host

    Args:
        target (str): IP address or hostname to scan
        port (int): Port number to scan
        timeout (float): Connection timeout in seconds

    Returns:
        bool: True if port is open, False otherwise
    """
        # TODO: Create a socket
        # TODO: Set timeout
        # TODO: Try to connect to target:port
        # TODO: Close the socket
        # TODO: Return True if connection successful

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)

        result = s.connect_ex((target, port))
        if result == 0:
            banner = ""
            try:
                banner = s.recv(1024).decode().strip()
            except:
                banner = "No banner"
            s.close()
            return port, banner
        s.close()
    except:
        pass
    return None

def scan_range(target, start_port, end_port,threads=50):
    """
    Scan a range of ports on the target host

    Args:
        target (str): IP address or hostname to scan
        start_port (int): Starting port number
        end_port (int): Ending port number

    Returns:
        list: List of open ports
    """
    open_ports = []

    print(f"[*] Scanning {target} from port {start_port} to {end_port}")
    print(f"[*] This may take a while...")

    # TODO: Implement the scanning logic
    # Hint: Loop through port range and call scan_port()
    # Hint: Consider using threading for better performance

        # TODO: Scan this port
        # TODO: If open, add to open_ports list
        # TODO: Print progress (optional)
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {
            executor.submit(scan_port, target, port): port
            for port in range(start_port, end_port + 1)
        }

        for future in as_completed(futures):
            result = future.result()
            if result:
                port, banner = result
                print(f"[OPEN] Port {port} - {banner}")
                open_ports.append(port)

    return open_ports



def main():
    """Main function"""
    # TODO: Parse command-line arguments
    # TODO: Validate inputs
    # TODO: Call scan_range()
    # TODO: Display results

    parser = argparse.ArgumentParser(description="Simple Port Scanner")
    parser.add_argument("--target", required=True, help="Target IP or hostname")
    parser.add_argument("--ports", default="1-1024", help="Port range (e.g. 1-1000)")
    parser.add_argument("--threads", type=int, default=50, help="Number of threads")

    args = parser.parse_args()

    try:
        start_port, end_port = map(int, args.ports.split("-"))
    except:
        print("Invalid port range. Use format: start-end (e.g. 1-1000)")
        sys.exit(1)

    print(f"[*] Starting port scan on {args.target}")

    open_ports = scan_range(args.target, start_port, end_port, args.threads)

    print(f"\n[+] Scan complete!")
    print(f"[+] Found {len(open_ports)} open ports:")
    for port in open_ports:
        print(f"    Port {port}: open")



if __name__ == "__main__":
    main()
