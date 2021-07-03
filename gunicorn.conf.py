import os

PORT = os.getenv("PORT", "5000")
BIND = "0.0.0.0:" + PORT
WORKERS = 1
LOG_LEVEL = "info"
