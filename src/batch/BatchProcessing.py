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
        
        for email in senderEmailAdresses:
            self.processEmail(email)

    def areEmailsFromFlood(self, emails, emailsCount):
        counter = 0
        while (counter + EMAIL_CHUNKS_LENGTH) < emailsCount:
            timestampDiff = abs(int(emails._current_rows[counter].timestamp) - int(emails._current_rows[counter + EMAIL_CHUNKS_LENGTH].timestamp))
            
            print(timestampDiff)
            counter += 1

    def processEmail(self, email):
        emailsResponse = self.cassandraMasterDataset.execute(f"select * from emails where sender='{email}' ALLOW FILTERING;")
        emailsCount = len(emailsResponse._current_rows)

        isFlood = self.areEmailsFromFlood(emailsResponse, emailsCount)
        print(isFlood)
        #for emailResponse in emailsResponse:
            #print(emailResponse.sender)
        #os.kill()
        #FUCK THIS SHIT!