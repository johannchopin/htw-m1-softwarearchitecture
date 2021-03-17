#!/bin/bash
# @author: flololan
# 

# [[ $EUID -ne 0 ]] && echo "This script must be run as root. Please run it with sudo" && exit 1

# Callback called
exit_script() {
    # Exiting and killing all 
    echo 'Exiting...'
    for job in $(jobs -p)
    do
        kill $job 2> /dev/null # Sends SIGTERM to child/sub processes
    done
    # Clean docker
    docker stop cassandra_b > /dev/null
    docker rm cassandra_b > /dev/null
    trap - SIGHUP SIGQUIT SIGTERM SIGINT SIGTERM # clear the trap
    exit 1
}

trap exit_script SIGHUP SIGQUIT SIGTERM SIGINT SIGTERM

echo '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Welcome to the BigData - Lambda Architecture - Demo'
echo 'This demo has been made by:'
echo 'Johann Chopin, Quentin Duflot, Alexandre Guidoux and Florian Weiss'
echo 'Please check the README for installation instructions'
echo '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
echo

echo 'Remove the running container and previous image'
docker stop cassandra_b 2> /dev/null
docker rm cassandra_b 2> /dev/null

echo 'Building the cassandra image'
docker build -t cassandra-batch src/batch > /dev/null

echo 'Starting the cassandra container'
docker run -d -p 9042:9042 --name cassandra_b cassandra-batch > /dev/null

echo 'Wait until the cassandra DB responds. This can take some time.'
python3 ./src/batch/CassandraHealthcheck.py
RC=$?
while [ $RC -eq 1 ]
do
    sleep 0.1
    python3 src/batch/CassandraHealthcheck.py
    RC=$?
done

echo 'Starting sender...'
python3 -m src.entry.sender -q &
sleep 2

echo 'Starting receiver...'
python3 -m src.entry.receiver -q &
sleep 1

echo 'Starting the batch processing'
python3 -m src.batch.BatchProcessing -q &

echo 'Starting API -- sudo is needed to run flask on a specific port'
export FLASK_RUN_PORT=2020
cd src && python3 -m flask run --host=127.0.0.1 &

echo 'Launching the dashboard...'
cd website && npm i && npm run dev