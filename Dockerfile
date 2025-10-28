# Use Python 3.10 slim as base image
FROM python:3.10-slim

# Set working directory in container
WORKDIR /app

# Copy requirements.txt first to leverage Docker layer caching
COPY catty-reminders-app/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy entire application code into container
COPY catty-reminders-app/ .

# Create directory for database if needed
RUN mkdir -p /app/data

# Expose port 8181 (port where the application runs)
EXPOSE 8181

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Health check to verify container is healthy (using stdlib, no requests needed)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; from urllib.request import urlopen; \
    try: \
        with urlopen('http://localhost:8181', timeout=5) as r: \
            sys.exit(0 if 200 <= r.status < 400 else 1) \
    except Exception: \
        sys.exit(1)"

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8181"]

