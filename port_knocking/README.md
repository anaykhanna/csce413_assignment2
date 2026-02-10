Port Knocking Implementation

Overview

This component implements a port knocking security mechanism to protect a hidden SSH service.
The protected port (2222) remains inaccessible until a client sends the correct sequence of connection attempts (knocks) to predefined ports.

Only after a valid knock sequence is received within a specified time window will the protected port be opened for the client’s IP address.


Design

Knock Sequence

Default knock sequence:

1234 → 5678 → 9012

The client must connect to these ports in the correct order within the allowed time window.

Protected Service
	•	Protected port: 2222
	•	Service: Secret SSH server
	•	Access is granted only after a valid knock sequence.

How It Works

Server Behavior

The port knocking server:
	1.	Listens on the knock sequence ports.
	2.	Tracks each client IP’s progress through the sequence.
	3.	Enforces a timing window for the sequence.
	4.	Resets progress on incorrect knocks or timeouts.
	5.	On a correct sequence:
	•	Opens port 2222 for the client IP using iptables.
	6.	Proxies connections from the client to the secret SSH server.


Client Behavior

The client:
	1.	Sends connection attempts to each port in the sequence.
	2.	Waits a short delay between knocks.
	3.	After completing the sequence, attempts to connect to the protected port.

How to run

Run the demo.sh file while also running the server

