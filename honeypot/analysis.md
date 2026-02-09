# Honeypot Analysis

## Observed Activity
Several simulated attack attempts were performed against the honeypot.

### Example Log Entries
Connection from 172.20.0.1:44336
Connection closed 172.20.0.1 duration=3.98s

Connection from 172.20.0.1:44358
Connection closed 172.20.0.1 duration=2.12s

## Observations
- Multiple login attempts were detected.
- All connections came from the same source IP during testing.
- Each connection lasted only a few seconds, indicating failed authentication attempts.

## Security Insights
- Attackers often try common usernames such as root and admin.
- Short connection durations suggest automated scanning tools.
- The honeypot successfully captured and logged these attempts.

## Conclusion
The honeypot effectively detected and logged unauthorized access attempts while appearing as a legitimate SSH service.
