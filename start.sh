# @author: flololan  
echo '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Welcome to the most advance Big Data-Project in the WORLD!'
echo 'I will start launching the Sender and receiver now... Please hold the lion!'
echo 'Doing some cleanup... You dirty little piece of shit
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
docker stop cassandra_b 2> /dev/null ;
docker rm cassandra_b 2> /dev/null ;
echo '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Building Cassandra-Image.... Just to make sure...
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
docker build -t cassandra-batch src/batch ;
echo '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Starting Cassandra-Batch-Container
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
docker run -d -p 9042:9042 --name cassandra_b cassandra-batch ;
echo '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Sleeping for 20 Seconds to let the slow pc start up everything...
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
sleep 20
#echo 'Starting PySpark'
#python src/batch/pyspark-processing &
 
echo '+++++++Okay... Lets go to work.... OH YEAH!+++++++'

echo '+++++++Starting sender...+++++++'
python3 -m src.entry.sender &
echo '+++++++Starting receiver...+++++++'
python3 -m src.entry.receiver &