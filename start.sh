# @author: flololan  
echo '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Welcome to the BigData - Lambda - Demo'
echo 'This demo has been made by:
 Johann Chopin, Quentin Duflot, Alexandre Guidoux and Florian Weiss'
echo '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Doing some cleanup....
'
docker stop cassandra_b 2> /dev/null ;
docker rm cassandra_b 2> /dev/null ;
echo '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Building Cassandra-Image.... Just to make sure it is up to date...
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
docker build -t cassandra-batch src/batch ;
echo '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Starting Cassandra-Batch-Container...
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
docker run -d -p 9042:9042 --name cassandra_b cassandra-batch ;
echo '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Sleeping for 20 Seconds to let the slow pc start up everything...
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
sleep 20
#echo 'Starting PySpark'
#python src/batch/pyspark-processing &
 
echo '+++++++Okay... Let us go to work....+++++++'

echo '+++++++Starting sender...+++++++'
python3 -m src.entry.sender &
echo '+++++++Starting receiver...+++++++'
python3 -m src.entry.receiver &