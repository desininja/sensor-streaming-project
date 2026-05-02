
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, avg
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType
import os


# Ensure Python prints immediately
os.environ['PYTHONUNBUFFERED'] = '1'

spark = SparkSession.builder \
    .appName("SensorDataProcessor") \
    .getOrCreate()

# HIDE THE INFO LOGS
spark.sparkContext.setLogLevel("WARN")

print("\n" + "="*40)
print("SPARK IS STARTING... WAITING FOR DATA")
print("="*40 + "\n")

schema = StructType([
    StructField("sensor_id", StringType()),
    StructField("distance_cm", IntegerType()),
    StructField("timestamp", DoubleType())
])


df = (spark
      .readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", "kafka:29092")
      .option("subscribe", "sensor-data")
      .option("startingOffsets", "latest")
      .load()
)

parsed_df = (df.selectExpr("CAST(value AS STRING)")
             .select(from_json(col("value"), schema).alias("data"))
             .select("data.*")
)


query = parsed_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()