#!/bin/bash
set -e

# Get PORT from environment variable or default to 8000
PORT=${PORT:-8000}

echo "Starting DevGenie API on 0.0.0.0:${PORT}"
echo "PORT environment variable: ${PORT}"

# Run uvicorn
exec uvicorn api:app --host 0.0.0.0 --port "${PORT}"

