from time import time
from .CassandraWrapper import CassandraWrapper


class CassandraViews (CassandraWrapper):
    LOG_TABLE = 'spamsCounterLog'
    SPAM_AMOUNT_DETECTED_BY_SPEED_TABLE = 'spamEmailAmountDetectedBySpeed'
    SPAM_AMOUNT_DETECTED_BY_BATCH_TABLE = 'spamEmailAmountDetectedByBatch'

    def __init__(self):
        self.spamsViewTableCounter = 0
        super().__init__()
        self._execute_silently(
            f"create table {self.getSpamsTableName()} ( email TEXT PRIMARY KEY);")
        self._execute_silently(
            f"create table {CassandraViews.LOG_TABLE} (timestamp TEXT PRIMARY KEY, spamCount BIGINT)")  # Related to addSpamLog
        self._execute_silently(
            f"create table {CassandraViews.SPAM_AMOUNT_DETECTED_BY_SPEED_TABLE} (timestamp TEXT PRIMARY KEY, spamCount BIGINT)")
        self._execute_silently(
            f"create table {CassandraViews.SPAM_AMOUNT_DETECTED_BY_BATCH_TABLE} (timestamp TEXT PRIMARY KEY, spamCount BIGINT)")

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

    def addSpamLog(self, timestamp: int, spamCount: int):
        self.execute(
            f"INSERT INTO {CassandraViews.LOG_TABLE}(timestamp, spamCount) VALUES ('{timestamp}', {spamCount})")

    def addSpamAmountDetectedBySpeed(self, amount):
        now = int(time() * 10**6)
        self.execute(
            f"INSERT INTO {CassandraViews.SPAM_AMOUNT_DETECTED_BY_SPEED_TABLE}(timestamp, spamCount) VALUES ('{now}', {amount})")

    def addSpamAmountDetectedByBatch(self, amount):
        now = int(time() * 10**6)
        self.execute(
            f"INSERT INTO {CassandraViews.SPAM_AMOUNT_DETECTED_BY_BATCH_TABLE}(timestamp, spamCount) VALUES ('{now}', {amount})")

CassandraViewsInstance = CassandraViews()
