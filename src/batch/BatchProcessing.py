from ..serving.CassandraViews import CassandraViewsInstance
import os

EMAIL_CHUNKS_LENGTH = 20
EMAIL_TIMESTAMP_LIMIT = 2 * 10^6 # TODO: Lol name

class BatchProcessing:
    def __init__(self, masterDatasetCassandraInstance):
        self.cassandraMasterDataset = masterDatasetCassandraInstance
        self.cassandraViews = CassandraViewsInstance
    
    def getSendersEmailAdress(self):
        sendersResponse = self.cassandraMasterDataset.execute("SELECT sender FROM emails;")
        
        distinctSender = set()

        for sender in sendersResponse:
            distinctSender.add(sender.sender)

        return distinctSender

    def process(self):
        # async shit
        senderEmailAdresses = self.getSendersEmailAdress()
        
        for emailAdress in senderEmailAdresses:
            self.processEmail(emailAdress)

    def areEmailsFromFlood(self, emails, emailsCount):
        counter = 0
        while (counter + EMAIL_CHUNKS_LENGTH) < emailsCount:
            timestampDiff = abs(int(emails._current_rows[counter].timestamp) - int(emails._current_rows[counter + EMAIL_CHUNKS_LENGTH].timestamp))
            if timestampDiff <= EMAIL_TIMESTAMP_LIMIT:
                return True
            counter += 1
        return False

    def processEmail(self, emailAddress):
        emailsResponse = self.cassandraMasterDataset.execute(f"select * from emails where sender='{emailAddress}' ALLOW FILTERING;")
        emailsCount = len(emailsResponse._current_rows)

        isFlood = self.areEmailsFromFlood(emailsResponse, emailsCount)
        if isFlood:
            print(emailAddress)
            #self.cassandraViews.execute(f"INSERT INTO {self.cassandraViews.getSpamsTableName()}(email) VALUES('{emailAddress}')")
            return
        # TODO: detect if the body content of emails have spam keywords
        #for emailResponse in emailsResponse:
            #print(emailResponse.sender)
        #os.kill()
        #FUCK THIS SHIT!

if __name__ == "__main__":
    from CassandraWrapper import CassandraWrapper
    batchProcessing = BatchProcessing(CassandraWrapper())
    batchProcessing.process()
