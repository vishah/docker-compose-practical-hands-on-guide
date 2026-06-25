import os
import socket

from flask import Flask


app = Flask(__name__)


@app.get("/")
def index():
    return {
        "message": os.getenv(
            "MESSAGE",
            "Edit app.py or compose.yaml and refresh to see the change",
        ),
        "hostname": socket.gethostname(),
        "mode": os.getenv("APP_MODE", "development"),
    }


@app.get("/health")
def health():
    return {"status": "ok"}
