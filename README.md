# htw-m1-softwarearchitecture

## Set up
## Virtual Environment for python
```bash
# Create Venv 
python -m venv .venv
# Use the virtual environment
source .venv/bin/activate
# Install listed dependencies
python -m pip install -r requiremetns.txt
# Export dependancies
python -m pip freeze > requirements.txt
# Exit venv
deactivate
```

### Batch Layer (cd into batch folder first)
Build cassandra image: `docker build -t cassandracustom .`
Run cassandra image: `docker run -d -p 9042:9042 --name cassandra cassandracustom`
Set up image: 
```bash
docker exec -it cassandra-batch bash
cqlsh
# create cassandra's keyspace
create keyspace lambda WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};
use lambda;
# create table emails
create table emails ( id TEXT PRIMARY KEY, sender TEXT, receiver TEXT, timestamp TIMESTAMP, subject TEXT, body TEXT);
exit
exit
```
Or fast
```bash
docker exec -it cassandra-batch bash
cqlsh --execute "create keyspace lambda WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3}; use lambda; create table emails ( id TEXT PRIMARY KEY, sender TEXT, receiver TEXT, timestamp TIMESTAMP, subject TEXT, body TEXT);"
```