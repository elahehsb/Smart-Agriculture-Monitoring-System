from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, avg
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

def main():
    spark = SparkSession.builder \
        .appName("Agriculture Analysis") \
        .getOrCreate()

    schema = StructType([
        StructField("timestamp", DoubleType(), True),
        StructField("temperature", DoubleType(), True),
        StructField("humidity", DoubleType(), True),
        StructField("soil_moisture", DoubleType(), True)
    ])

    kafka_df = spark.readStream.format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "agriculture") \
        .load()

    sensor_df = kafka_df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*")

    avg_df = sensor_df.groupBy().agg(
        avg("temperature").alias("avg_temperature"),
        avg("humidity").alias("avg_humidity"),
        avg("soil_moisture").alias("avg_soil_moisture")
    )

    query = avg_df.writeStream \
        .outputMode("complete") \
        .format("console") \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    main()
