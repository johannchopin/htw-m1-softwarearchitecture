from typing import List
from ..serving.CassandraViews import CassandraViewsInstance
from ..EmailChecker import EmailChecker



class SpeedLayer:
    def __init__(self):
        self.cassandra = CassandraViewsInstance
        self.emailChecker = EmailChecker()

    def process_email(self, email):
        print(self.is_spam(email))
        pass

    def _read_spam_keywords(self, filePath) -> List[str]:
        with open(filePath, 'r') as f:
            return [keyword for keyword in f if keyword]

    def is_spam(self, email):
        is_sender_in_spam_view = self.is_sender_in_spam_view(
            email['sender'])
        isEmailContainingSpamWords = self.emailChecker.isSpam(email)
        return is_sender_in_spam_view or isEmailContainingSpamWords

    def is_sender_in_spam_view(self, email):
        matching_email_count = self.cassandra.execute(f"""
        SELECT email from spams where email='{email}';
        """)
        return len(matching_email_count._current_rows)
