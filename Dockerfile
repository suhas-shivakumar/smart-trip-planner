
FROM python:3.11-slim-bullseye

# Set working directory
WORKDIR /app

# Install system dependencies and supervisord
RUN apt-get update && apt-get install -y \
    build-essential \
    supervisor \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port for FastAPI (default: 8000)
EXPOSE 8000

# Set environment variables (optional)
# ENV PYTHONUNBUFFERED=1

# --- Option 1: Use shell script to start both services ---
# Uncomment the following line to use the shell script approach:
CMD ["bash", "start_services.sh"]

# --- Option 2: Use supervisord to start both services ---
# Uncomment the following line to use supervisord approach:
# CMD ["supervisord", "-c", "/app/supervisord.conf"]
