
---

# 🚀 IoT Real-Time Streaming Pipeline: Arduino to Kafka, Spark & Flink

A full-stack data engineering project that captures physical distance data using an **Arduino Uno** and an **HC-SR04 Ultrasonic Sensor**, streams it through **Apache Kafka**, and processes it simultaneously using **Apache Flink** (Real-time layer) and **Apache Spark** (Micro-batch layer).

## 🏗️ Architecture Overview

![Architecture Diagram](Architecture%20Diagram.png)

The project implements a **Lambda Architecture** to demonstrate two different processing paradigms:

1.  **The Edge Layer:** Arduino Uno captures distance data and sends it via Serial to a Python Bridge.
2.  **The Ingestion Layer:** A Python-based Kafka Producer pushes structured JSON to a Kafka Broker.
3.  **The Speed Layer (Flink):** Provides millisecond-latency processing for immediate alerts.
4.  **The Batch Layer (Spark):** Aggregates data into structured micro-batches for analytical reporting.

---

## 🔌 Hardware Setup

### Components
*   Arduino Uno R3
*   HC-SR04 Ultrasonic Sensor
*   Jumper Wires & Breadboard

### Connection Guide
![Arduino UNO Setup](Arduino%20UNO.png)

### Wiring Diagram
| HC-SR04 Pin | Arduino Pin |
| :--- | :--- |
| VCC | 5V |
| GND | GND |
| TRIG | Pin 9 |
| ECHO | Pin 10 |

### Arduino Firmware
Flash the firmware located at `Arduino Uno sketch/MeasureDistance.cpp` using the Arduino IDE. It outputs raw JSON strings to the Serial port every 3 seconds to ensure clean parsing by the Kafka bridge.

---

## 🐳 Software Infrastructure (Docker)

The analytical stack is fully containerized and orchestrated using `docker-compose`. It features **automatic topic provisioning** and **health-aware dependency management**.

### Services:
*   **Kafka (KRaft Mode):** Modern Kafka 4.0.0 cluster without Zookeeper.
*   **Kafka-Init:** A bootstrap container that ensures the `sensor-data` topic exists before consumers start.
*   **PySpark Consumer:** Structured Streaming job that processes data into micro-batches.
*   **Flink JobManager/TaskManager:** Event-driven engine for real-time sensor monitoring.

### Deployment
```bash
# 1. Start the entire analytical cluster
docker compose up -d

# 2. Verify infrastructure health
docker compose ps
```
*Note: The cluster uses a dual-listener configuration (Port 9092 for external host access, Port 29092 for internal container-to-container traffic).*

---

## 🐍 The Ingestion Bridge

Since Docker on macOS runs in a VM, it cannot access USB ports directly. We use a local Python gateway to bridge the physical sensor to the virtual cluster.

**Prerequisites:**
```bash
pip install kafka-python-ng pyserial
```

**Run the Bridge:**
```bash
python3 python-ingestor/main.py
```

---

## 📊 Analytical Outputs

### Apache Flink (The Speed Layer)
Flink treats every sensor reading as an individual event. 
*   **Log Check:** `docker logs -f flink-taskmanager`
*   **Expected Output:** `Distance Alert: arduino_hc_sr04 is 12 cm away`

### Apache Spark (The Batch Layer)
Spark groups events into windows for structural analysis.
*   **Log Check:** `docker logs -f pyspark-consumer`
*   **Expected Output:**
```text
-------------------------------------------
Batch: 5
-------------------------------------------
+-----------------+-----------+-------------------+
|    sensor_id    |distance_cm|     timestamp     |
+-----------------+-----------+-------------------+
|arduino_hc_sr04  |     15    |2026-05-02 20:45:01|
+-----------------+-----------+-------------------+
```

---

## 🛠️ Key Engineering Features Implemented
*   **Self-Healing:** Consumers use `restart: always` and depend on a `service_completed_successfully` state from the Kafka-init container.
*   **Schema Enforcement:** Rigid schema definition in PySpark using `StructType` to ensure data quality.
*   **Modern Kafka:** Implementation of KRaft (Kafka Raft) mode, moving away from legacy Zookeeper dependencies.
*   **Dual-Network Listeners:** Sophisticated Docker networking allowing simultaneous communication from both the host machine and internal containers.

---
Developed by Himanshu Bhatt