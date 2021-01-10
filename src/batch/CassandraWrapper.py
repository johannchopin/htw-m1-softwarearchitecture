# pip install cassandra-driver
from cassandra.cluster import Cluster
from .singleton import singleton


@singleton
class CassandraWrapper:
    def __init__(self):
        self.cluster = Cluster(['127.0.0.1'], port=9042)
        self.session = self.cluster.connect('lambda', wait_for_all_pools=True)
        self.session.execute('USE lambda')

    def execute(self, query):
        self.session.execute(query)


if __name__ == "__main__":
    # Test Singleton
    cassandra = CassandraWrapper()
    cassandra2 = CassandraWrapper()
    assert cassandra is cassandra2
    print(cassandra.execute())
