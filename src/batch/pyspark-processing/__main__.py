import os
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages com.datastax.spark:spark-cassandra-connector_2.12:3.0.0 --conf spark.cassandra.connection.host=127.0.0.1 pyspark-shell'

sc = SparkContext("local", "PySpark email processing")
sqlContext = SQLContext(sc)

sqlContext.read.format("org.apache.spark.sql.cassandra").options(
    table="emails", keyspace="lambda").load().show()
