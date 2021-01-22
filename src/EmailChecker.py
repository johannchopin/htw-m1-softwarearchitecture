import os
from .entry import Email


class EmailChecker:
    def __init__(self):
        dirname = os.path.dirname(__file__)
        spamKeywordsFilePath = os.path.join(dirname, './Spam_Keywords.txt')
        with open(spamKeywordsFilePath, 'r') as f:
            self.keywords = [keyword for keyword in f if keyword]

    def isSpam(self, email: Email):
        spam_word_counter = 0
        for item in self.keywords:
            if item in email["body"]:
                spam_word_counter += 1
        return spam_word_counter >= len(email["body"].split()) / 100
