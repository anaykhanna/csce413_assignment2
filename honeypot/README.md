SSH Honeypot

Overview
This project implements a simple SSH honeypot that simulates a real SSH service and logs unauthorized access attempts. The honeypot listens for incoming SSH connections, presents a realistic SSH banner, and records all interaction data. The goal is to attract attackers, monitor their behavior, and collect security information without exposing a real system.

Features
The honeypot simulates an SSH server and sends a realistic SSH banner when a client connects. It logs all connection attempts and records the source IP address, source port, timestamp, connection duration, and any data sent by the client. The entire honeypot runs inside a Docker container to keep it isolated from the host system.

File Structure
The honeypot directory contains the Dockerfile for container setup, honeypot.py as the main implementation, logger.py for logging support, README.md for the project description, analysis.md for attack analysis, and a logs directory where connection logs are stored.

How It Works
The honeypot listens on port 22 inside the container. Docker maps host port 2222 to the container’s port 22. When a client connects, the honeypot sends an SSH banner to appear like a real SSH service. It records the connection details, logs any data received from the client, and then closes the connection. All activity is stored in the honeypot log file.

Testing the Honeypot
Attack attempts can be simulated by trying to connect to the honeypot using different usernames. The connection will close automatically because it is not a real SSH server. These attempts will still be recorded in the logs.

Logs
All connection activity is recorded in the honeypot log file. The logs include connection attempts, any data sent by the client, and the duration of each session.

Conclusion
This honeypot successfully simulates an SSH service, captures connection attempts, and logs attacker behavior. It provides a simple but effective way to observe unauthorized access attempts in a controlled environment.
