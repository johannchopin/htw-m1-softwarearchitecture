from sys import exit
from CassandraWrapper import CassandraWrapper

try:
    CassandraWrapper()
except:
    exit(1)

exit(0)
