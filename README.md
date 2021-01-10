# htw-m1-softwarearchitecture

## Set up
### Batch Layer
Build cassandra image: `docker built -t cassandracustom batch`
Run cassandra image: `docker run -d -p 9042:9042 --name cassandra cassandracustom`
Set up image: 
```bash
docker exec -it cassandra-batch bash
cqlsh
# create cassandra's keyspace
create keyspace lambda WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};
use lambda;
# create emails table
create table emails ( id TEXT PRIMARY KEY, sender TEXT, receiver TEXT, timestamp TIMESTAMP, subject TEXT, body TEXT);
exit
exit
```
Or fast
```bash
docker exec -it cassandra-batch bash
cqlsh --execute "create keyspace lambda WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3}; use lambda; create table emails ( id TEXT PRIMARY KEY, sender TEXT, receiver TEXT, timestamp TIMESTAMP, subject TEXT, body TEXT);"
```