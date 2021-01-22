from .CassandraWrapper import CassandraWrapper


class CassandraViews (CassandraWrapper):
    def __init__(self):
        self.spamsViewTableCounter = 0
        super().__init__()
        self._execute_silently(
            f"create table {self.getSpamsTableName()} ( email TEXT PRIMARY KEY);")

    def init_next_table(self):
        self._execute_silently(
            f"create table {self.getNextSpamsTableName()} ( email TEXT PRIMARY KEY);")

    def use_next_table(self):
        self.spamsViewTableCounter += 1
        self.drop_previous_spams_view_table()

    def drop_previous_spams_view_table(self):
        self.execute(f'DROP TABLE spams{self.spamsViewTableCounter - 1};')

    def getSpamsTableName(self):
        return f"spams{self.spamsViewTableCounter}"

    def getNextSpamsTableName(self):
        return f"spams{self.spamsViewTableCounter+1}"


CassandraViewsInstance = CassandraViews()
