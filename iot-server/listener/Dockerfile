FROM python:3.10-slim

WORKDIR /app

RUN pip install paho-mqtt influxdb-client requests

COPY listener.py .

# Agrega -u para unbuffered output
CMD ["python", "-u", "listener.py"]
