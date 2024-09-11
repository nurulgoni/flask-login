# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y \
        pkg-config \
        libmariadb-dev \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

COPY entrypoint.sh /app/

# Make entrypoint.sh executable
RUN chmod +x entrypoint.sh

# Expose port 5000
EXPOSE 5000

# Use the custom entry point script
ENTRYPOINT ["./entrypoint.sh"]


