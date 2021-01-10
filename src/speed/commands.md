## Create cassandra bdd

```speed
$ cqlsh

# create cassandra's keyspace
$ create keyspace lambda WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};

$ use lambda;

# create addresses table
$ create table addresses ( id TEXT PRIMARY KEY, sender TEXT, is_spam BOOLEAN);
```