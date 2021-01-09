import json
from faker import Faker
from random import randint, choice
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
    reciever: EmailAddress
    timestamp: int
    subject: str
    content: str


# class EmailJsonEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, Email):
#             return obj.__dict__
#         # Base class default() raises TypeError:
#         return json.JSONEncoder.default(self, obj)


def generateEmailAdresses(amount: int) -> List[EmailAddress]:
    return [FAKE.email() for _ in range(amount)]


def generateEmailContent(nb_max_paragraph=3, nb_max_sentences_per_paragraph=10) -> str:
    """ Generate the body of an email, i.e. the message """
    paragraph_amount = range(randint(1, nb_max_paragraph))
    return '\n'.join((FAKE.paragraph(
        nb_sentences=nb_max_sentences_per_paragraph,
        variable_nb_sentences=True
    ) for _ in paragraph_amount))


def getTimestamp(precision_after_second=6, additional_seconds=0):
    """
        Helper that return a timestamp, with additional seconds if provided
        The returned timestamp is in ms (10^-6s)
    """
    shift_after_seconds = 10**precision_after_second
    return int(time() * shift_after_seconds + additional_seconds * shift_after_seconds)


def generateSimpleEmail(emailAdresses: List[EmailAddress], withTimestamp=None) -> Email:
    """" Generate a fake email from a list of email address, a custom timestamp cam be provided """
    sender = choice(emailAdresses)
    reciever = choice(emailAdresses)
    timestamp = withTimestamp if withTimestamp else getTimestamp()
    subject = FAKE.sentence(nb_words=5)
    content = generateEmailContent(nb_max_paragraph=5)
    return Email(sender, reciever, timestamp, subject, content)


if __name__ == "__main__":
    print(emails)
