#!/bin/sh
$CASSANDRA_HOME/bin/cassandra -fR
cqlsh --execute "create keyspace lambda WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};"
echo "Create keyspace: $?"
cqlsh --execute "create table lambda.emails ( id TEXT PRIMARY KEY, sender TEXT, receiver TEXT, timestamp TIMESTAMP, subject TEXT, body TEXT);"
echo "Create email table: $?"