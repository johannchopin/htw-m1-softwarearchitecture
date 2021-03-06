import json
import os
from faker import Faker
from random import randint, choice, random
from dataclasses import dataclass
from typing import NewType, List
from time import time


FAKE = Faker()
# Fake.seed()

_SPAM_WORDLIST_SOURCE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'Spam_Keywords.txt')
SPAM_WORDLIST = [word.strip() for word in open(_SPAM_WORDLIST_SOURCE)]

EmailAddress = NewType('EmailAdress', str)


@dataclass
class Email:
    """ Structure of an email """
    sender: EmailAddress
    receiver: EmailAddress
    timestamp: int
    subject: str
    body: str


class EmailJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Email):
            return obj.__dict__
        # Base class default() raises TypeError:
        return json.JSONEncoder.default(self, obj)


def generateEmailAdresses(amount: int) -> List[EmailAddress]:
    return [FAKE.email() for _ in range(amount)]


def generateEmailBody(nb_max_paragraph=3, nb_max_sentences_per_paragraph=10) -> str:
    """ Generate the body of an email, i.e. the message """
    paragraph_amount = range(randint(1, nb_max_paragraph))
    return '\n'.join((FAKE.paragraph(
        nb_sentences=nb_max_sentences_per_paragraph,
        variable_nb_sentences=True
    ) for _ in paragraph_amount))


def getTimestamp(precision_after_second=3):
    """
        Helper that return a timestamp, with additional seconds if provided
        The returned timestamp is in ms (10^-3s)
    """
    shift_after_seconds = 10**precision_after_second
    return int(time() * shift_after_seconds)


def generateSpamBody(emailBody: str) -> str:
    global SPAM_WORDLIST
    SPAM_WORD_AFTER_N_WORDS = 10

    words = emailBody.split()
    for i in range(0, len(words), SPAM_WORD_AFTER_N_WORDS):
        words[i] = choice(SPAM_WORDLIST)

    return ' '.join(words)


def generateSimpleEmail(emailAdresses: List[EmailAddress], spammerAdresses=[], spam_rate=0.0, from_sender='', with_body=False) -> Email:
    """" Generate a fake email from a list of email address, a custom sender and body message can be provided (for flood) """
    sender = choice(emailAdresses) if not from_sender else from_sender
    receiver = choice(emailAdresses)
    timestamp = getTimestamp()
    subject = FAKE.sentence(nb_words=5)
    body = generateEmailBody(
        nb_max_paragraph=5) if not with_body else with_body
    if random() < spam_rate:
        sender = choice(spammerAdresses)
        body = generateSpamBody(body)
    return Email(sender, receiver, timestamp, subject, body)


def generateFloodEmail(emailAdresses, emailGeneratedCount):
    flooder_adress = choice(emailAdresses)
    body = generateEmailBody(nb_max_paragraph=5)
    return (generateSimpleEmail(emailAdresses, from_sender=flooder_adress, with_body=body) for _ in range(emailGeneratedCount))


def generateEmails(emailAdresses: List[EmailAddress], spammerAdresses=[], spam_rate=0.0, flood_rate=0.0, *, email_amount=0):
    emails = []
    if random() < flood_rate:
        emails.extend(generateFloodEmail(
            spammerAdresses, email_amount))  # randint(0, email_amount)
    else:
        email_amount_left = email_amount - len(emails)
        emails.extend((generateSimpleEmail(emailAdresses=emailAdresses, spammerAdresses=spammerAdresses, spam_rate=spam_rate)
                       for _ in range(email_amount_left)))
    return emails


if __name__ == "__main__":
    print(generateSpamBody(generateEmailBody(
        nb_max_paragraph=5)))
