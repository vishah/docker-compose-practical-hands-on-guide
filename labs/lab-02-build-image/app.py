import os
import socket

from flask import Flask


app = Flask(__name__)


@app.get("/")
def index():
    return {
        "message": os.getenv("MESSAGE", "Hello from Docker"),
        "hostname": socket.gethostname(),
        "mode": os.getenv("APP_MODE", "standalone"),
    }


@app.get("/health")
def health():
    return {"status": "ok"}
