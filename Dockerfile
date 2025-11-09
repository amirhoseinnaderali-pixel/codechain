FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Make start script executable
RUN chmod +x start.sh start.py

# Expose port (Railway will set PORT env var)
EXPOSE 8000

# Run the application using Python script (more reliable)
CMD ["python", "api.py"]

