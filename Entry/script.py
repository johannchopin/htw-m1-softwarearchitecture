from fakeEmails import Email, generateEmailAdresses, generateSimpleEmail, getTimestamp
from pathlib import Path
from datetime import datetime
from time import sleep


def recieveEmail(emailAdressPool, path: Path):
    EMAIL_CONTENT_DIR_NAME_INDEX_SPLIT = 3

    email = generateSimpleEmail(emailAdressPool)
    email_content_hash = str(abs(hash(email.subject + email.content)))
    date = datetime.fromtimestamp(email.timestamp / 1_000_000)

    (year, month, day) = (str(date.year), str(
        date.month).rjust(2, '0'), str(date.day).rjust(2, '0'))
    metadata_fullpath = path.joinpath('meta').joinpath(
        year).joinpath(month).joinpath(day)
    email_content_fullpath = path.joinpath(
        'content').joinpath(email_content_hash[:EMAIL_CONTENT_DIR_NAME_INDEX_SPLIT])

    if not metadata_fullpath.exists():
        metadata_fullpath.mkdir(parents=True)

    with open(metadata_fullpath.joinpath(str(email.timestamp)), 'a+') as f:
        f.write(f"{email.sender} {email.reciever} {email_content_hash}")

    if not email_content_fullpath.exists():
        email_content_fullpath.mkdir(parents=True)

    with open(email_content_fullpath.joinpath(email_content_hash[EMAIL_CONTENT_DIR_NAME_INDEX_SPLIT:]), 'a+') as f:
        f.write(f"{email.subject}\n\n{email.content}")


if __name__ == "__main__":
    # Set up
    DATA_PATH = Path("./data")
    emails = generateEmailAdresses(50)

    # Generate Emails
    while True:
        sleep(0.1)
        recieveEmail(emails, DATA_PATH)
