FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port (Railway will set PORT env var)
EXPOSE 8000

# Run the application (use PORT env var or default to 8000)
# Using shell form to access environment variable
CMD uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000}


