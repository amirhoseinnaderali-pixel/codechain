#!/usr/bin/env python3
import os
import sys
import subprocess

# Get PORT from environment variable or default to 8000
port = int(os.getenv("PORT", 8000))

print(f"Starting DevGenie API on 0.0.0.0:{port}")
print(f"PORT environment variable: {port}")

# Run uvicorn
cmd = [
    "uvicorn",
    "api:app",
    "--host", "0.0.0.0",
    "--port", str(port)
]

sys.exit(subprocess.run(cmd).returncode)

