## Create cassandra bdd

```bash
$ cqlsh

# create cassandra's keyspace
$ create keyspace lambda WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};

$ use lambda;

# create emails table
$ create table emails ( id TEXT PRIMARY KEY, sender TEXT, receiver TEXT, timestamp TIMESTAMP, subject TEXT, body TEXT);
```
