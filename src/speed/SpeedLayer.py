import os
from typing import List
from ..serving.CassandraViews import CassandraViewsInstance


class SpeedLayer:
    def __init__(self):
        self.cassandra = CassandraViewsInstance
        self.dictionary = self.read_suspicious_keywords_dictionnary(
            self.get_keywords_filepath())

    def get_keywords_filepath(self):
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, '../Spam_Keywords.txt')

    def process_email(self, email):
        # print(self.is_spam(email))
        pass

    def is_spam(self, email):
        is_sender_in_spam_view = self.is_sender_in_spam_view(
            email['sender'])
        is_spam_by_wordlist = self.is_spam_by_wordlist(
            self.dictionary, email)
        return is_sender_in_spam_view or is_spam_by_wordlist

    def is_sender_in_spam_view(self, email):
        matching_email_count = self.cassandra.execute(f"""
        SELECT email from spams where email='{email}';
        """)
        return len(matching_email_count._current_rows)

    def read_suspicious_keywords_dictionnary(self, filePath) -> List[str]:
        with open(filePath, 'r') as f:
            return [keyword for keyword in f if keyword]

    def is_spam_by_wordlist(self, list_dictionary, email):
        for item in list_dictionary:
            if item in email["body"]:
                spam_word_counter += 1
        return spam_word_counter >= len(email["body"].split()) / 2
