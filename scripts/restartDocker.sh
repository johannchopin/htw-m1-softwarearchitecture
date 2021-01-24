[[ $EUID -ne 0 ]] && echo "This script must be run as root." && exit 1
echo '
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Doing some cleanup....
'
docker stop cassandra_b 2> /dev/null ;
docker rm cassandra_b 2> /dev/null ;
echo 'Installing dependencies....'


echo '
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Building Cassandra-Image.... Just to make sure it is up to date...
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'
docker build -t cassandra-batch src/batch ;
echo '
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Starting Cassandra-Batch-Container...
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'
docker run -d -p 9042:9042 --name cassandra_b cassandra-batch ;
echo '
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Sleeping for 20 Seconds to let the slow pc start up everything...
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'
sleep 20 ;
echo '
DONE
'