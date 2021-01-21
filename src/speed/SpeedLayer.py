import os
from typing import List
from ..serving.CassandraViews import CassandraViewsInstance


class SpeedLayer:
    def __init__(self):
        self.cassandra = CassandraViewsInstance
        self.keywordSourceFile = self.get_keywords_filepath()
        self.keyword_list = self._read_spam_keywords(self.keywordSourceFile)

    def get_keywords_filepath(self):
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, '../Spam_Keywords.txt')

    def process_email(self, email):
        # print(self.is_spam(email))
        pass

    def _read_spam_keywords(self, filePath) -> List[str]:
        with open(filePath, 'r') as f:
            return [keyword for keyword in f if keyword]

    def is_spam(self, email):
        is_sender_in_spam_view = self.is_sender_in_spam_view(
            email['sender'])
        is_spam_by_wordlist = self.is_spam_by_wordlist(
            self.keyword_list, email)
        return is_sender_in_spam_view or is_spam_by_wordlist

    def is_sender_in_spam_view(self, email):
        matching_email_count = self.cassandra.execute(f"""
        SELECT email from spams where email='{email}';
        """)
        return len(matching_email_count._current_rows)

    def is_spam_by_wordlist(self, list_dictionary, email):
        for item in list_dictionary:
            if item in email["body"]:
                spam_word_counter += 1
        return spam_word_counter >= len(email["body"].split()) / 2
