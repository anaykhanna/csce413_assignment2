FROM python:3.11-slim

WORKDIR /app


RUN apt-get update \
    && apt-get install -y --no-install-recommends iptables iproute2 \
    && rm -rf /var/lib/apt/lists/*

COPY knock_server.py .
COPY knock_client.py .
COPY demo.sh .


RUN chmod +x demo.sh


CMD ["python3", "knock_server.py"]


