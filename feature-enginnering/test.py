from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("TestApp") \
    .master("local[*]") \
    .getOrCreate()

df = spark.createDataFrame([(1, "foo"), (2, "bar")], ["id", "value"])
df.show()

spark.stop()
