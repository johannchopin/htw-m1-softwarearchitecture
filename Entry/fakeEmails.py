from faker import Faker
from random import randint, choice
from dataclasses import dataclass
from typing import NewType, List
from time import time

FAKE = Faker()
# Fake.seed()

EmailAddress = NewType('EmailAdress', str)


@dataclass(frozen=True)
class Email:
    """ Structure of an email """
    sender: EmailAddress
    reciever: EmailAddress
    timestamp: int
    content: str


def generateEmailAdresses(amount: int) -> List[EmailAddress]:
    return [FAKE.email() for _ in range(amount)]


def generateEmailContent(nb_max_paragraph=3, nb_max_sentences_per_paragraph=10) -> str:
    """ Generate the body of an email, i.e. the message """
    paragraph_amount = range(randint(1, nb_max_paragraph))
    return '\n'.join((FAKE.paragraph(
        nb_sentences=nb_max_sentences_per_paragraph,
        variable_nb_sentences=True
    ) for _ in paragraph_amount))


def getTimestamp(precision_after_second=6):
    return int(time() * 10**precision_after_second)


def generateSimpleEmail(emailAdresses: List[EmailAddress]) -> Email:
    """" Generate a fake email from a list of email address """
    sender = choice(emailAdresses)
    reciever = choice(emailAdresses)
    content = generateEmailContent(nb_max_paragraph=5)
    timestamp = getTimestamp()
    return Email(sender, reciever, timestamp, content)


if __name__ == "__main__":
    emailAdresses = generateEmailAdresses(50)
    print(generateSimpleEmail(emailAdresses))
