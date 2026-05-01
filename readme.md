---

# Real-Time IoT Analytics Pipeline: Spark vs. Flink

An end-to-end Data Engineering ecosystem that compares the two industry-leading stream processing engines. This project ingests live sensor data (Mock or Physical Arduino Uno) into **Apache Kafka** and processes it simultaneously using **Apache Spark Structured Streaming** and **Apache Flink**.



## 🚀 Key Features
- **Hybrid Processing:** Concurrent execution of Micro-batch (Spark) and Native Streaming (Flink).
- **Polyglot Architecture:** Real-time consumers implemented in both **Python** and **Java**.
- **Hardware Integration:** Support for physical **Arduino Uno** sensors via a Serial-to-Kafka bridge.
- **Full Orchestration:** Single-command deployment using Docker Compose.

## 🛠 Tech Stack
- **Infrastructure:** Apache Kafka (KRaft mode), Docker, Docker Compose
- **Processing:** Apache Spark 3.5 (PySpark), Apache Flink 1.18 (Java/Maven)
- **Ingestion:** Python 3.9 (pyserial, kafka-python-ng)
- **Hardware:** Arduino Uno (ATmega328P)

## 📦 Project Structure
```text
sensor-streaming-project/
├── flink-processor/      # Java Flink Consumer (Maven-based)
├── pyspark-consumer/     # PySpark Structured Streaming Consumer
├── python-ingestor/      # Data Producer (Mock or Hardware Bridge)
└── docker-compose.yml    # Full Cluster Orchestration
```

## 🚦 Getting Started (macOS)

### 1. Launch Infrastructure
Initialize the Kafka broker and both consumers:
```bash
docker compose up --build
```

### 2. Monitor Output
*   **Spark (Micro-batch):** `docker logs -f pyspark-consumer`
*   **Flink (Event-driven):** `docker logs -f flink-taskmanager`
*   **Web UI:** Monitor Flink's execution graph at [http://localhost:8081](http://localhost:8081).

### 3. Physical Hardware (Optional)
To use a real Arduino Uno, stop the mock ingestor and run the local bridge:
```bash
docker compose stop ingestor
python3 bridge.py # Connects /dev/cu.usbmodem to localhost:9092
```

## 📊 Observations: Spark vs. Flink
| Feature | Apache Spark | Apache Flink |
| :--- | :--- | :--- |
| **Model** | Micro-batching | Continuous Streaming |
| **Latency** | Seconds (Configurable) | Sub-millisecond |
| **Language** | PySpark (Ease of use) | Java (Performance/Type-safe) |
| **Use Case** | Complex ETL / ML | Low-latency alerts / Fraud detection |

---