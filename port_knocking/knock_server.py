#!/usr/bin/env python3
"""Starter template for the port knocking server."""

import argparse
import logging
import socket
import time
import subprocess


DEFAULT_KNOCK_SEQUENCE = [1234, 5678, 9012]
DEFAULT_PROTECTED_PORT = 2222
DEFAULT_SEQUENCE_WINDOW = 10.0

import threading
import select

authorized_ips = {}

def pipe(a, b):
    sockets = [a, b]
    while True:
        r, _, _ = select.select(sockets, [], [], 30)
        if not r:
            return
        for src in r:
            dst = b if src is a else a
            data = src.recv(4096)
            if not data:
                return
            dst.sendall(data)




def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )


def open_protected_port(protected_port, source_ip):
    """Open the protected port using firewall rules."""
    # TODO: Use iptables/nftables to allow access to protected_port
    logging.info("Opening port %s for %s", protected_port, source_ip)
    subprocess.run([
        "iptables",
        "-I", "INPUT",
        "-p", "tcp",
        "--dport", str(protected_port),
        "-s", source_ip,
        "-j", "ACCEPT"
    ])

def close_protected_port(protected_port, source_ip):
    """Close the protected port using firewall rules."""
    # TODO: Remove firewall rules for protected_port.
    logging.info("Closing port %s for %s", protected_port, source_ip)
    subprocess.run([
        "iptables",
        "-D", "INPUT",
        "-p", "tcp",
        "--dport", str(protected_port),
        "-s", source_ip,
        "-j", "ACCEPT"
    ])


def listen_for_knocks(sequence, window_seconds, protected_port):
    """Listen for knock sequence and open the protected port."""
    logger = logging.getLogger("KnockServer")
    logger.info("Listening for knocks: %s", sequence)
    logger.info("Protected port: %s", protected_port)

    # TODO: Create UDP or TCP listeners for each knock port.
    # TODO: Track each source IP and its progress through the sequence.
    # TODO: Enforce timing window per sequence.
    # TODO: On correct sence, call open_protected_port().
    # TODO: On incorrect sequence, reset progress.
    knock_progress = {}

    sockets = []
    for port in sequence:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", port))
        s.listen(5)
        sockets.append((port, s))
        logger.info("Listening on port %s", port)


    gate = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    gate.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    gate.bind(("0.0.0.0", protected_port))
    gate.listen(5)
    logger.info("Gate listening on port %s", protected_port)


    while True:
        for port, sock in sockets:
            sock.settimeout(0.2)
            try:
                conn, addr = sock.accept()
                ip = addr[0]
                conn.close()

                now = time.time()
                index, last_time = knock_progress.get(ip, (0, 0))

                if now - last_time > window_seconds:
                    index = 0

                if port == sequence[index]:
                    index += 1
                    if index == len(sequence):
                        logger.info("Correct sequence from %s", ip)
                        open_protected_port(protected_port, ip)
                        index = 0
                else:
                    index = 0

                knock_progress[ip] = (index, now)

            except socket.timeout:
                pass

        gate.settimeout(0.2)
        try:
            client, addr = gate.accept()
            ip = addr[0]

            logger.info("Forwarding SSH for %s", ip)
            backend = socket.create_connection(("172.20.0.20", 2222))
            threading.Thread(target=pipe, args=(client, backend)).start()

        except socket.timeout:
            pass

def parse_args():
    parser = argparse.ArgumentParser(description="Port knocking server starter")
    parser.add_argument(
        "--sequence",
        default=",".join(str(port) for port in DEFAULT_KNOCK_SEQUENCE),
        help="Comma-separated knock ports",
    )
    parser.add_argument(
        "--protected-port",
        type=int,
        default=DEFAULT_PROTECTED_PORT,
        help="Protected service port",
    )
    parser.add_argument(
        "--window",
        type=float,
        default=DEFAULT_SEQUENCE_WINDOW,
        help="Seconds allowed to complete the sequence",
    )
    return parser.parse_args()

def main():
    args = parse_args()
    setup_logging()

    try:
        sequence = [int(port) for port in args.sequence.split(",")]
    except ValueError:
        raise SystemExit("Invalid sequence. Use comma-separated integers.")

    listen_for_knocks(sequence, args.window, args.protected_port)


if __name__ == "__main__":
    main()
