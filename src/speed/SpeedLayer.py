
from src.entry.fakeEmails import Email

class SpeedLayer:

    def process_email(self, email: Email):
        print(self.contains_mail_suspicious_keyword(email))

    def contains_mail_suspicious_keyword(email: Email):
        if "fuckfuckfuck" in email.body:
            return True
        return False

    def is_sender_spamming(email: Email):
        '''
        TODO: Check in the views if the sending adress is known for spamming
        '''
        return False