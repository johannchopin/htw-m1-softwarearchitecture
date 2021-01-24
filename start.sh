# @author: flololan  
[[ $EUID -ne 0 ]] && echo "This script must be run as root." && exit 1
echo '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Welcome to the BigData - Lambda - Demo'
echo 'This demo has been made by:
 Johann Chopin, Quentin Duflot, Alexandre Guidoux and Florian Weiss'
echo 'Please check readme for installation instructions'
echo '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Doing some cleanup....
'
docker stop cassandra_b 2> /dev/null ;
docker rm cassandra_b 2> /dev/null ;
echo 'Installing dependencies....'


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
echo
echo 'Waiting again... Sorry for that. How is you day so far?'
sleep 5
echo '+++++++Starting Batch processing++++++++'
python3 -m src.batch.BatchProcessing &
echo 'Starting API'
cd src && sudo python3 -m flask run --host=127.0.0.1 --port=2020 &
cd ..
echo
echo 'Launching our beautiful dashboard...'
npm run dev --prefix website 

