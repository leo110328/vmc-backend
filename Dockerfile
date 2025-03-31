FROM python:3.10-slim

WORKDIR /opt/vmc-backend

# Install required system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make scripts executable
RUN chmod +x docker-entrypoint.sh
RUN chmod +x run.sh
RUN chmod +x init_db.py

# Create data directory for file uploads
RUN mkdir -p /opt/data

# Expose the application port
EXPOSE 8000

# Set up entrypoint script
CMD ["./docker-entrypoint.sh"] 