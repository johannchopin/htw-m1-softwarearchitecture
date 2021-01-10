# 2. Data Generation - master dataset structure

Date: 2021-01-03

## Status

Accepted

## Context and Decision

The master dataset structure and the associated generated data will change often in this project. To keep things in order, this ADR is the reference that explains the generation of the fake data and the structure of the master dataset.

## Generating the fake data

The library Faker handles the generation of the following data:
* email addresses (from real provider; with random user name)
* email subject as one random sentence
* email body as a random sequence of sentences, grouped as paragraph
* the current timestamp as integer in ms

A fake email sent is done by selecting two email adresses randomly, the rest is retrieved from Faker.

The dataclass `Email` describes all metadata:
```python
@dataclass
class Email:
    """ Structure of an email """
    sender: EmailAddress
    receiver: EmailAddress
    timestamp: int
    subject: str
    body: str
```

## Structure of the master dataset

Each email is stored in two places:
* the metadata are represented on one line per unique email: `sender_email receiver_email timestamp_in_ms hash_id`
  * stored in `data/meta/YYYY/MM/DD/X` with X an number starting from 1
  * each text file regroup 10 000 lines of email
* the `hash_id` is used to retrieve the subject and body of the email from the text file: `subject\n\nbody`
  * stored in `data/body/XXX/YYYYYYYYYYYYYYYY` with XXX are the first 3 digits of the `hash_id`, and YYYY... the rest of them
  * the subject is written on one line
  * the body can be of any length
  