import os
import socket

import redis
from flask import Flask


app = Flask(__name__)


def get_client():
    return redis.Redis(
        host=os.getenv("REDIS_HOST", "redis"),
        port=int(os.getenv("REDIS_PORT", "6379")),
        decode_responses=True,
    )


@app.get("/")
def index():
    redis_status = "connected"
    hits = None

    try:
        hits = get_client().incr("hits")
    except redis.exceptions.RedisError as exc:
        redis_status = f"error: {exc}"

    return {
        "message": os.getenv(
            "MESSAGE",
            "Hello from the production-ish Compose lab",
        ),
        "hostname": socket.gethostname(),
        "mode": os.getenv("APP_MODE", "productionish"),
        "redis_status": redis_status,
        "hit_count": hits,
    }


@app.get("/health")
def health():
    try:
        get_client().ping()
        return {"status": "ok"}
    except redis.exceptions.RedisError as exc:
        return {"status": "error", "error": str(exc)}, 500
