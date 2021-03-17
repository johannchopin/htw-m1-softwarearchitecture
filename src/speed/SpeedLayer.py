from typing import List
from cassandra import InvalidRequest
from ..serving.CassandraViews import CassandraViewsInstance
from ..EmailChecker import EmailChecker


class SpeedLayer:
    def __init__(self):
        self.detectedSpamCount = 0
        self.cassandra = CassandraViewsInstance
        self.emailChecker = EmailChecker()
        self.emailAdresses = set()

    def process_email(self, email):
        if self.is_spam(email):
            print(f"Spam detected in Speed layer from {email['sender']}")
            self.detectedSpamCount += 1
            self.storeDetectedSpamCountInView()
            self.emailAdresses.add(email['sender'])

    def storeDetectedSpamCountInView(self):
        if self.detectedSpamCount % 10 == 0:
            self.cassandra.addSpamAmountDetectedBySpeed(self.detectedSpamCount)

    def _read_spam_keywords(self, filePath) -> List[str]:
        with open(filePath, 'r') as f:
            return [keyword for keyword in f if keyword]

    def is_spam(self, email):
        is_sender_in_spam_view = self.is_sender_in_spam_view(
            email['sender'])
        isEmailContainingSpamWords = self.emailChecker.isSpam(email)
        return is_sender_in_spam_view or isEmailContainingSpamWords

    def is_sender_in_spam_view(self, email):
        try:
            matching_email_count = self.cassandra.execute(f"""
            SELECT email from {self.cassandra.getSpamsTableName()} where email='{email}';
            """)
        except InvalidRequest:
            self.cassandra.spamsViewTableCounter += 1
            return self.is_sender_in_spam_view(email)
        return len(matching_email_count._current_rows) > 0
