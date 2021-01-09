# htw-m1-softwarearchitecture

## Set up
### Batch Layer
Build cassandra image: `docker built -t cassandracustom batch`
Run cassandra image: `docker run -d -p 9042:9042 --name cassandra cassandracustom`