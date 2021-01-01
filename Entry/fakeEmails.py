from faker import Faker
from random import randint, choice
from dataclasses import dataclass
from typing import NewType, List

FAKE = Faker()

EmailAddress = NewType('EmailAdress', str)


@dataclass
class Email:
    """ Structure of an email """
    sender: EmailAddress
    reciever: EmailAddress
    content: str


def generateEmailAdresses(amount: int) -> List[EmailAddress]:
    return [FAKE.email() for _ in range(amount)]


def generateEmailContent(nb_max_paragraph=3, nb_max_sentences_per_paragraph=10) -> str:
    paragraph_amount = range(randint(1, nb_max_paragraph))
    return '\n'.join((FAKE.paragraph(
        nb_sentences=nb_max_sentences_per_paragraph,
        variable_nb_sentences=True
    ) for _ in paragraph_amount))


def generateSimpleEmail(emailAdresses: List[EmailAddress]) -> Email:
    sender = choice(emailAdresses)
    reciever = choice(emailAdresses)
    content = generateEmailContent(nb_max_paragraph=5)
    return Email(sender, reciever, content)


if __name__ == "__main__":
    emailAdresses = generateEmailAdresses(50)
    print(generateSimpleEmail(emailAdresses))
