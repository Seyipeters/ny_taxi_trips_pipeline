FROM python:3.9-slim

#Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

#copy requirements.txt to the container
COPY requirements.txt .

#install required python packages
RUN pip install --no-cache-dir -r requirements.txt

#Copy the python scripts into the container
COPY ingest_taxi_data.py .
COPY ny-taxi-trips-pipeline-9640b65ea078.json /tmp/service-account-file.json

#Set environment variables for the credentials file
ENV GOOGLE_APPLICATION_CREDENTIALS=/tmp/service-account-file.json

#Set the default command to run the python script
ENTRYPOINT ["python", "ingest_taxi_data.py"]