import os

PORT = os.getenv("PORT", "8080")
BIND = "0.0.0.0:" + PORT
WORKERS = 1
LOG_LEVEL = "info"
