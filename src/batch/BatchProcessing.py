import os
import sys
from time import time
from typing import Set
from datetime import datetime
from ..EmailChecker import EmailChecker
from ..serving.CassandraViews import CassandraViewsInstance
from .CassandraWrapper import CassandraWrapper

EMAIL_CHUNKS_LENGTH = 200
EMAIL_SENT_TIMESTAMP_LIMIT = 30
PERCENTAGE_OF_SPAMS_TO_BLACKLIST = 0.2

if '-q' in sys.argv:
    sys.stdout = open(os.devnull, 'w')


class BatchProcessing:
    def __init__(self, masterDatasetCassandraInstance):
        self.emailChecker = EmailChecker()
        self.cassandraMasterDataset = masterDatasetCassandraInstance
        self.cassandraViews = CassandraViewsInstance
        self.spamSenderCount = 0
        self.spamEmailsCount = 0

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

            timestamp = int(time() * 10**6)
            self.cassandraViews.addSpamLog(timestamp, self.spamSenderCount)
            self.cassandraViews.addSpamAmountDetectedByBatch(
                self.spamEmailsCount)

            self.spamSenderCount = 0  # reset counter
            self.spamEmailsCount = 0  # reset counter
            self.cassandraViews.use_next_table()
            print("Batch process finished")

    def areEmailsFromFlood(self, emails, emailsCount):
        # TODO: refactor to for loop
        counter = 0
        while (counter + EMAIL_CHUNKS_LENGTH) < emailsCount:
            timestamp1 = emails._current_rows[counter].timestamp.timestamp()
            timestamp2 = emails._current_rows[counter +
                                              EMAIL_CHUNKS_LENGTH].timestamp.timestamp()
            if self._timestamp_diff(timestamp1, timestamp2) <= EMAIL_SENT_TIMESTAMP_LIMIT:
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
            self.spamSenderCount += 1  # An email has been detected as spam
            self.spamEmailsCount += emailsCount
        else:
            oneSpamHasBeenDetected = False
            for email in emailsResponse:
                if self.emailChecker.isSpam({'body': email.body}):
                    oneSpamHasBeenDetected = True
                    self.spamEmailsCount += 1
            if oneSpamHasBeenDetected:
                self.insert_email_into_spam_view(emailAddress)
                self.spamSenderCount += 1  # An email has been detected as spam

    def insert_email_into_spam_view(self, emailAddress):
        self.cassandraViews.execute(
            f"INSERT INTO {self.cassandraViews.getNextSpamsTableName()}(email) VALUES('{emailAddress}')")

    def _timestamp_diff(self, timestamp1: float, timestamp2: float) -> int:
        return int(abs(timestamp1 - timestamp2) * 10**3)


if __name__ == "__main__":
    batchProcessing = BatchProcessing(CassandraWrapper())
    batchProcessing.process()
