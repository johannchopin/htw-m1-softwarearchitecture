from fakeEmails import Email, generateEmailAdresses, generateSimpleEmail, getTimestamp
from pathlib import Path
from datetime import datetime
from time import sleep


def _mkdir_if_not_exists(path: Path):
    if not path.exists():
        path.mkdir(parents=True)


def recieveEmail(emailAdressPool, path: Path):
    INDEX_SPLIT = 3

    email = generateSimpleEmail(emailAdressPool)
    email_content_hash = str(abs(hash(email.subject + email.content)))
    date = datetime.fromtimestamp(email.timestamp / 1_000_000)

    (year, month, day) = (str(date.year), str(
        date.month).rjust(2, '0'), str(date.day).rjust(2, '0'))

    metadata_fullpath = path.joinpath('meta').joinpath(
        year).joinpath(month).joinpath(day)
    _mkdir_if_not_exists(metadata_fullpath)
    with open(metadata_fullpath.joinpath(str(email.timestamp)), 'a+') as f:
        f.write(f"{email.sender} {email.reciever} {email_content_hash}")

    email_content_fullpath = path.joinpath(
        'content').joinpath(email_content_hash[:INDEX_SPLIT])
    _mkdir_if_not_exists(email_content_fullpath)
    with open(email_content_fullpath.joinpath(email_content_hash[INDEX_SPLIT:]), 'a+') as f:
        f.write(f"{email.subject}\n\n{email.content}")


if __name__ == "__main__":
    # Set up
    DATA_PATH = Path("./data")
    emails = generateEmailAdresses(50)

    # Generate Emails
    while True:
        sleep(0.1)
        recieveEmail(emails, DATA_PATH)
