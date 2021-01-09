# pip install cassandra-driver
from cassandra.cluster import Cluster


class CassandraWrapper:
    def __init__(self):
        self.cluster = Cluster(['127.0.0.1'], port=9042)
        self.session = self.cluster.connect('lambda', wait_for_all_pools=True)
        self.session.execute('USE lambda')
