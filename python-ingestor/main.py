import time
import json
import random 
from kafka import KafkaProducer


# connect to kafka container using the service name from docker-compose

print("Producer waiting for Kafka...")
while True:
    try:
        producer = KafkaProducer(
            bootstrap_servers=['kafka:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            request_timeout_ms=5000  # Try for 5 seconds
        )
        break # Exit loop if connection is successful
    except Exception as e:
        print(f"Kafka not ready yet... retrying in 2 seconds. ({e})")
        time.sleep(2)

print("Connected! Sending data...")

try:
    while True:
        #Simulate data
        data = {
            "sensor_id": "arduino_01",
            "temperature":round(random.uniform(20.0,30.0),2),
            "humidity": round(random.uniform(40.0, 60.0), 2),
            "timestamp": time.time()
        }

        producer.send("sensor-data",value=data)
        print(f"Sent: {data}")
        time.sleep(3)

except KeyboardInterrupt:
    print("Stopping Kafka Producer.")

finally:
    producer.close()