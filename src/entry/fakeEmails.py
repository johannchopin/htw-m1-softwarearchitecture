import json
from faker import Faker
from random import randint, choice, random
from dataclasses import dataclass
from typing import NewType, List
from time import time

# TODO: Add suspicious keywords

FAKE = Faker()
# Fake.seed()

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


def getTimestamp(precision_after_second=6):
    """
        Helper that return a timestamp, with additional seconds if provided
        The returned timestamp is in ms (10^-6s)
    """
    shift_after_seconds = 10**precision_after_second
    return int(time() * shift_after_seconds)


def generateSpamBody(emailBody: str) -> str:
    return emailBody + " fuckfuckfuck"


def generateSimpleEmail(emailAdresses: List[EmailAddress], spam_rate=0.0, from_sender='', with_body=False) -> Email:
    """" Generate a fake email from a list of email address, a custom sender and body message can be provided (for flood) """
    sender = choice(emailAdresses) if not from_sender else from_sender
    receiver = choice(emailAdresses)
    timestamp = getTimestamp()
    subject = FAKE.sentence(nb_words=5)
    body = generateEmailBody(
        nb_max_paragraph=5) if not with_body else with_body
    if random() < spam_rate:
        body = generateSpamBody(body)
    return Email(sender, receiver, timestamp, subject, body)


def generateFloodEmail(emailAdresses, emailGeneratedCount):
    flooder_adress = choice(emailAdresses)
    body = generateEmailBody(nb_max_paragraph=5)
    return (generateSimpleEmail(emailAdresses, from_sender=flooder_adress, with_body=body) for _ in range(emailGeneratedCount))


def generateEmails(emailAdresses: List[EmailAddress], spam_rate=0.0, flood_rate=0.0, *, email_amount=0):
    emails = []
    if random() < flood_rate:
        emails.extend(generateFloodEmail(
            emailAdresses, randint(0, email_amount)))

    email_amount_left = email_amount - len(emails)
    emails.extend((generateSimpleEmail(emailAdresses, spam_rate)
                   for _ in range(email_amount_left)))
    return emails


if __name__ == "__main__":
    print('main')
