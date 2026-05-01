FROM bitnami/spark:3.5.0

USER root
WORKDIR /app

# Install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY spark_processor.py .

# Explicitly use local[*] to run Spark inside this container
CMD ["spark-submit", \
     "--master", "local[*]", \
     "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0", \
     "spark_processor.py"]