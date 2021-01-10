# Example File
# Source: https://realpython.com/pyspark-intro/
# https://max6log.wordpress.com/2020/05/25/introduction-to-pyspark-on-docker/

import pyspark

sc = pyspark.SparkContext('local[*]')
sqlContext = pyspark.SQLContext(sc)

# Loads and returns data frame for a table including key space given
def load_and_get_table_df(keys_space_name, table_name):
    table_df = sqlContext.read\
        .format("org.apache.spark.sql.cassandra")\
        .options(table=table_name, keyspace=keys_space_name)\
        .load()
    return table_df

mails = load_and_get_table_df("lambda", "email")
mails.show() 