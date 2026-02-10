Honeypot Attack Analysis

Overview

An SSH honeypot was deployed in a Docker container and exposed on port 2222 of the host system. Several connection attempts were simulated using different usernames to imitate unauthorized access attempts. All activity was recorded by the honeypot logs.


Source of Connections

All recorded connections came from the IP address:

172.20.0.1

This indicates the traffic originated from the local host machine or another container on the same Docker network. This matches the simulated attack commands executed locally.

Observed Behavior

The honeypot detected multiple SSH connection attempts. Each connection:
	•	Originated from the same IP address
	•	Used different temporary source ports
	•	Sent an SSH client banner during the handshake

Example captured banner:

SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.13

This is the default identification string sent by an SSH client when attempting to connect to a server.


Attack Pattern

The following behavior was observed:

Attempt 1
Source IP: 172.20.0.1
Connection duration: about 2 seconds
No significant data sent

Attempt 2
Source IP: 172.20.0.1
SSH client banner received
Connection closed immediately

Attempt 3
Source IP: 172.20.0.1
SSH client banner received
Connection closed immediately

Attempt 4
Source IP: 172.20.0.1
SSH client banner received
Connection closed immediately

This pattern indicates repeated login attempts, which is typical of automated SSH probing or brute-force scripts.


Security Observations
	•	Multiple connections from the same IP within a short time window may indicate suspicious behavior.
	•	Repeated short connections suggest automated scanning tools.
	•	The honeypot successfully captured connection details and SSH banners without exposing a real service.

Conclusion

The honeypot successfully logged unauthorized SSH connection attempts. It recorded:
	•	Source IP addresses
	•	Connection timestamps
	•	Connection durations
	•	Data sent by the client

The results demonstrate that the honeypot is effective at detecting and recording suspicious activity.
