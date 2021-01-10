FROM cassandra
COPY cassandra-env.sh /etc/cassandra
# COPY cassandra-entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh && ./entrypoint.sh
RUN cqlsh --execute "create keyspace lambda WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3}; use lambda; create table emails ( id TEXT PRIMARY KEY, sender TEXT, receiver TEXT, timestamp TIMESTAMP, subject TEXT, body TEXT);"
EXPOSE 9042

