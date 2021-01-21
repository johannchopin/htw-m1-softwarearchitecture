import os
from typing import Set
from datetime import datetime
from dateutil import parser as datetimeParser
# from ..serving.CassandraViews import CassandraViewsInstance

EMAIL_CHUNKS_LENGTH = 20
EMAIL_SENT_LIMIT_IN_INTERVAL = 2 * 10 ^ 6


class BatchProcessing:
    def __init__(self, masterDatasetCassandraInstance):
        self.cassandraMasterDataset = masterDatasetCassandraInstance
        # self.cassandraViews = CassandraViewsInstance

    def getSendersEmailAdress(self) -> Set[str]:
        sendersResponse = self.cassandraMasterDataset.execute(
            "SELECT sender FROM emails;")

        return {response.sender for response in sendersResponse}

    def process(self):
        # async shit
        senderEmailAdresses = self.getSendersEmailAdress()

        for emailAdress in senderEmailAdresses:
            self.processEmail(emailAdress)

    def areEmailsFromFlood(self, emails, emailsCount):
        counter = 0
        while (counter + EMAIL_CHUNKS_LENGTH) < emailsCount:
            timestamp1 = emails._current_rows[counter].timestamp
            timestamp2 = emails._current_rows[counter +
                                              EMAIL_CHUNKS_LENGTH].timestamp
            if self._timestamp_diff(timestamp1, timestamp2) <= EMAIL_SENT_LIMIT_IN_INTERVAL:
                return True
            counter += 1
        return False

    def processEmail(self, emailAddress):
        emailsResponse = self.cassandraMasterDataset.execute(
            f"select * from emails where sender='{emailAddress}' ALLOW FILTERING;")
        emailsCount = len(emailsResponse._current_rows)

        isFlood = self.areEmailsFromFlood(emailsResponse, emailsCount)
        if isFlood:
            # self.cassandraViews.execute(f"INSERT INTO {self.cassandraViews.getSpamsTableName()}(email) VALUES('{emailAddress}')")
            print(emailAddress)
            return
        # TODO: detect if the body content of emails have spam keywords
        # for emailResponse in emailsResponse:
            # print(emailResponse.sender)
        # os.kill()
        # FUCK THIS SHIT !

    def _timestamp_diff(self, timestamp1: datetime, timestamp2: datetime) -> bool:
        return abs(timestamp1.microsecond - timestamp2.microsecond)


if __name__ == "__main__":
    from CassandraWrapper import CassandraWrapper
    batchProcessing = BatchProcessing(CassandraWrapper())
    batchProcessing.process()
