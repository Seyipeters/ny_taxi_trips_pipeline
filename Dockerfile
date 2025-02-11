FROM python:3.9-slim

# Set the working directory
WORKDIR /app

#copy requirements.txt to the container
COPY requirements.txt .

#install required python packages
RUN pip install --no-cache-dir -r requirements.txt

#Copy the python scripts and the schemas to the container
COPY . .

#Set environment variables for bigquery credentials
ENV GOOGLE_APPLICATION_CREDENTIALS="/app//Keys/ny-taxi-trips-pipeline-407ec6dc6c8d.json"

#Comman to run the ingestion script (default for yellow taxi; can be overridden)
CMD ["python", "ingest_yellow_taxi.py"]

