import os
from ..serving.CassandraViews import CassandraViewsInstance

class SpeedLayer:
    def __init__(self):
        self.cassandra = CassandraViewsInstance
        self.dictionary = self.read_suspicious_keywords_dictionnary(self.get_keywords_filepath())

    def get_keywords_filepath(self):
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, '../Spam_Keywords.txt')

    def process_email(self, email):
        print(self.is_spam(email))

    def is_spam(self, email):
        contains_mail_suspicious_keyword = self.contains_mail_suspicious_keyword(email)
        is_sender_spammer_in_views = self.is_sender_spammer_in_views(email['sender'])
        check_spam_with_dictionary = self.check_spam_with_dictionary(self.dictionary, email)
        return contains_mail_suspicious_keyword or is_sender_spammer_in_views or check_spam_with_dictionary

    def contains_mail_suspicious_keyword(self, email):
        return "fuckfuckfuck" in email['body']

    def is_sender_spammer_in_views(self, email):
        matching_email_count = self.cassandra.execute(f"""
        SELECT email from spams where email='{email}';
        """)
        return len(matching_email_count._current_rows)

    def read_suspicious_keywords_dictionnary(self, filePath):
        file = open(filePath, 'r')
        list = []
        while True:
            line = file.readline()
            if not line:
                break
            list.append(line)
        return list

    def check_spam_with_dictionary(self, list_dictionary, email):
        spam_word_counter = 0
        for item in list_dictionary:
            if item in email["body"]:
                spam_word_counter += 1
        return spam_word_counter >= len(email["body"].split()) / 2
