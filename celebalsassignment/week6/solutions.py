// initializing SparkSession
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType

spark = SparkSession.builder.appName("Week6").getOrCreate()

df = spark.read.csv("source.csv", header=True, inferSchema=True)
df.show(5)
df.printSchema()

# Q5
df.select("product_id", "price") \ .filter(col("category") == "Electronics")

# Q6
from pyspark.sql.types import DoubleType
df = df.withColumnRenamed("old_name", "new_name")
df = df.withColumn("price",col("price").cast(DoubleType()))

# Q8
df_orders.filter((col("status") == "Completed") &(col("amount") > 1000))

# Q10
df = df.withColumn("final_price",col("base_price") * 1.18)

# Q12
df = spark.read.parquet("path/to/input")
df.filter(col("user_id").isNotNull()).write.csv(
    "path/to/output",header=True,mode="overwrite")

# Q14
df.filter((col("region") == "North") | (col("priority") == "High"))