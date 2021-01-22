import os
from typing import Set
from datetime import datetime
from dateutil import parser as datetimeParser
from ..EmailChecker import EmailChecker
from ..serving.CassandraViews import CassandraViewsInstance
from .CassandraWrapper import CassandraWrapper

EMAIL_CHUNKS_LENGTH = 20
EMAIL_SENT_LIMIT_IN_INTERVAL = 2 * 10 ^ 6
PERCENTAGE_OF_SPAMS_TO_BLACKLIST = 0.2


class BatchProcessing:
    def __init__(self, masterDatasetCassandraInstance):
        self.emailChecker = EmailChecker()
        self.cassandraMasterDataset = CassandraWrapper()
        self.cassandraViews = CassandraViewsInstance

    def getSendersEmailAdress(self) -> Set[str]:
        sendersResponse = self.cassandraMasterDataset.execute(
            "SELECT sender FROM emails;")

        return {response.sender for response in sendersResponse}

    def process(self):
        while True:
            self.cassandraViews.init_next_table()
            senderEmailAdresses = self.getSendersEmailAdress()

            for emailAdress in senderEmailAdresses:
                self.processEmail(emailAdress)

            print(f"{self.cassandraViews.getSpamsTableName()} has been populated")
            self.cassandraViews.use_next_table()

    def areEmailsFromFlood(self, emails, emailsCount):
        # TODO: refactor to for loop
        counter = 0
        while (counter + EMAIL_CHUNKS_LENGTH) < emailsCount:
            timestamp1 = emails._current_rows[counter].timestamp
            timestamp2 = emails._current_rows[counter +
                                              EMAIL_CHUNKS_LENGTH].timestamp
            if self._timestamp_diff(int(timestamp1), int(timestamp2)) <= EMAIL_SENT_LIMIT_IN_INTERVAL:
                return True
            counter += 1
        return False

    def emailsContainsSpamWords(self, emails, emailsCount):
        emailContainingSpamWordsCounter = 0
        for i in range(emailsCount):
            emailBody = emails._current_rows[i].body
            email = {'body': emailBody}
            isSpam = self.emailChecker.isSpam(email)
            if isSpam:
                emailContainingSpamWordsCounter += 1
        # Blacklist if 20% of emails are a spam
        return (emailContainingSpamWordsCounter / emailsCount) > PERCENTAGE_OF_SPAMS_TO_BLACKLIST

    def processEmail(self, emailAddress):
        emailsResponse = self.cassandraMasterDataset.execute(
            f"select * from emails where sender='{emailAddress}' ALLOW FILTERING;")
        emailsCount = len(emailsResponse._current_rows)

        if self.areEmailsFromFlood(emailsResponse, emailsCount):
            self.insert_email_into_spam_view(emailAddress)
        else:
            for email in emailsResponse:
                if self.emailChecker.isSpam({'body': email.body}):
                    self.insert_email_into_spam_view(emailAddress)

    def insert_email_into_spam_view(self, emailAddress):
        self.cassandraViews.execute(
            f"INSERT INTO {self.cassandraViews.getNextSpamsTableName()}(email) VALUES('{emailAddress}')")

    def _timestamp_diff(self, timestamp1: int, timestamp2: int) -> bool:
        return abs(timestamp1 - timestamp2)


if __name__ == "__main__":
    batchProcessing = BatchProcessing(CassandraWrapper())
    batchProcessing.process()
