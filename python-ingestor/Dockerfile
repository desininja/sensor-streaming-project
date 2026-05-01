# Lightweight python base image
FROM python:3.11-slim

# setting work directory inside the container
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
# copy your local script into the container's app folder
COPY main.py .

# python command to run the script when container starts
CMD ["python", "main.py"]
