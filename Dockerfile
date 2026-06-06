FROM python:3.9-slim

#Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy requirements.txt to the container
COPY requirements.txt .

# Install required python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application script into the container
COPY ingest_taxi_data.py .

# Create a default output directory
RUN mkdir -p /app/data/processed

# Set the default command to run the python script
ENTRYPOINT ["python", "ingest_taxi_data.py"]