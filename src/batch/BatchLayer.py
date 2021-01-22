from ..batch import CassandraWrapper
from ..entry.fakeEmails import Email
from .BatchProcessing import BatchProcessing


class BatchLayer:
    def __init__(self):
        self.cassandra = CassandraWrapper()

    def process_email(self, email: Email):
        self._insert_email_in_db(email)

    def _get_email_id(self, email: Email):
        return email['sender'] + email['receiver'] + str(email['timestamp'])

    def _insert_email_in_db(self, email):
        self.cassandra.execute(f"""
        INSERT INTO emails(id, sender, receiver, timestamp, subject, body) \
                VALUES('{self._get_email_id(email)}', '{email['sender']}', '{email['receiver']}', '{email['timestamp']}', '{email['subject']}', '{email['body']};')
        """)
