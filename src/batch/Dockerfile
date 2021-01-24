FROM cassandra
COPY cassandra-env.sh /etc/cassandra
COPY docker-healthcheck /usr/local/bin/
HEALTHCHECK CMD ["docker-healthcheck"]
EXPOSE 9042

