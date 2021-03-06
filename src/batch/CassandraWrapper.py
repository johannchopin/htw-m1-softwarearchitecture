# pip install cassandra-driver
from cassandra import AlreadyExists
from cassandra.cluster import Cluster


class CassandraWrapper:
    def __init__(self, keyspace='lambda'):
        self.cluster = Cluster(['127.0.0.1'], port=9042)
        self.keyspace = keyspace
        self._setup_db()  # Create the keyspace
        self.session = self.cluster.connect('lambda', wait_for_all_pools=True)

    def execute(self, query):
        return self.session.execute(query)

    def _setup_db(self):
        self.session = self.cluster.connect('', wait_for_all_pools=True)
        self._execute_silently(
            f"create keyspace {self.keyspace} WITH replication = {{'class':'SimpleStrategy', 'replication_factor' : 3}};")
        self.execute(f"USE {self.keyspace}")
        self._execute_silently(
            "create table emails ( id TEXT PRIMARY KEY, sender TEXT, receiver TEXT, timestamp TIMESTAMP, subject TEXT, body TEXT);")

    def _execute_silently(self, query):
        try:
            self.execute(query)
        except AlreadyExists:
            # Silent error
            pass


if __name__ == "__main__":
    # Test Singleton
    cassandra = CassandraWrapper()
    cassandra2 = CassandraWrapper()
    assert cassandra is cassandra2
