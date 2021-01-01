from faker import Faker
from random import randint

FAKE = Faker()


def generateEmails(amount: int):
    return [FAKE.email() for _ in range(amount)]


def generateEmailContent(nb_max_paragraph=3, nb_max_sentences_per_paragraph=10):
    paragraph_amount = range(randint(1, nb_max_paragraph))
    return '\n'.join((FAKE.paragraph(
        nb_sentences=nb_max_sentences_per_paragraph,
        variable_nb_sentences=True
    ) for _ in paragraph_amount))


if __name__ == "__main__":
    print(generateEmailContent(nb_max_paragraph=10))
