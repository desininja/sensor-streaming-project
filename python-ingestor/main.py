import serial
import json
import time
from kafka import KafkaProducer

# Ensure this matches your 'ls /dev/cu.*' output
SERIAL_PORT = '/dev/cu.usbmodem12101' 

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    api_version=(3,4,1), # Be specific
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    acks=1, # Wait for leader to acknowledge
    retries=5
)

try:
    ser = serial.Serial(SERIAL_PORT, 9600, timeout=1)
    print(f"--- Connected to Arduino on {SERIAL_PORT} ---")
except Exception as e:
    print(f"Serial Error: {e}")
    print("Hint: Is the Arduino Serial Monitor closed?")
    exit()
try:

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            try:
                data = json.loads(line)
                data['timestamp'] = time.time()
            
                producer.send('sensor-data', value=data)
                print(f"Relayed to Kafka: {data}")
            except json.JSONDecodeError:
                # This handles the "Distance: 4 cm" vs JSON mismatch
                print(f"Raw data (not JSON): {line}")

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")
