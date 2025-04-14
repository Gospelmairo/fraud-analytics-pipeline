from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp
import os

# Prefer using environment variables instead of hardcoding secrets
AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]

# ✅ Create SparkSession with S3 support
spark = SparkSession.builder \
    .appName("FraudTransform") \
    .config("spark.jars.packages",
            "org.apache.hadoop:hadoop-aws:3.3.2,"
            "com.amazonaws:aws-java-sdk-bundle:1.12.375") \
    .getOrCreate()

# ✅ Set Hadoop AWS configs
hadoop_conf = spark._jsc.hadoopConfiguration()
hadoop_conf.set("fs.s3a.access.key", AWS_ACCESS_KEY)
hadoop_conf.set("fs.s3a.secret.key", AWS_SECRET_ACCESS_KEY)
hadoop_conf.set("fs.s3a.endpoint", "s3.amazonaws.com")
hadoop_conf.set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
hadoop_conf.set("com.amazonaws.services.s3.enableV4", "true")  # Optional, but can help

# ✅ Read CSV from S3
df = spark.read.option("header", "true").csv("s3a://mairo-g/transactions/synthetic_fraud_data.csv")

# ✅ Type casting and timestamp parsing
df_cleaned = df.withColumn("amount", col("amount").cast("double")) \
               .withColumn("timestamp", to_timestamp("timestamp")) \
               .withColumn("distance_from_home", col("distance_from_home").cast("double")) \
               .withColumn("transaction_hour", col("transaction_hour").cast("int")) \
               .withColumn("velocity_last_hour", col("velocity_last_hour").cast("int")) \
               .withColumn("is_fraud", col("is_fraud").cast("int"))

# ✅ Write to S3 as Parquet
df_cleaned.write.mode("overwrite").parquet("s3a://mairo-g/processed/transactions/")



spark.stop()

