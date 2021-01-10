
from src.entry.fakeEmails import Email


class SpeedLayer:

    def __init__(self):
        self.dictionary = self.read_suspicious_keywords_dictionnary('../Spam_Keywords.txt')

    def process_email(self, email: Email):
        print(self.is_spam(email))

    def is_spam(self, email: Email):
        contains_mail_suspicious_keyword = self.contains_mail_suspicious_keyword(email)
        is_sender_spamming = self.is_sender_spamming(email)
        check_spam_with_dictionary = self.check_spam_with_dictionary(self.dictionary, email)
        if contains_mail_suspicious_keyword or is_sender_spamming or check_spam_with_dictionary:
            return True
        else:
            return False

    def contains_mail_suspicious_keyword(email: Email):
        if "fuckfuckfuck" in email.body:
            return True
        return False

    def is_sender_spamming(email: Email):
        '''
        TODO: Check in the views if the sending adress is known for spamming
        '''
        return False

    def read_suspicious_keywords_dictionnary(filePath):
        file = open(filePath, 'r')
        list = []
        while True:
            line = file.readline()
            if not line:
                break
            list.append(line)
        return list

    def check_spam_with_dictionary(list_dictionary, email: Email):
        spam_word_counter = 0
        for item in list_dictionary:
            if item in email.body:
                spam_word_counter += 1
        if spam_word_counter >= len(email.body.split()) / 2:
            return True
        else:
            return False
