from .CassandraWrapper import CassandraWrapper

class CassandraViews (CassandraWrapper):
    def __init__(self):
        self.spamsViewTableCounter = 0
        super().__init__()
        self._execute_silently(
            f"create table {self.getSpamsTableName()} ( email TEXT PRIMARY KEY);")
    
    def getSpamsTableName(self):
        return f"spams{self.spamsViewTableCounter}"
    

CassandraViewsInstance = CassandraViews()
