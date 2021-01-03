import os
from pathlib import Path
from datetime import datetime
from time import sleep
from fakeEmails import Email, generateEmailAdresses, generateSimpleEmail, getTimestamp

MAX_LINE_IN_METADA_FILE = 10_000


def mkdir_if_not_exists(path: Path):
    if not path.exists():
        path.mkdir(parents=True)


def get_latest_filename(path: Path) -> int:
    return max(1, len(os.listdir(path)))


def record_metadata(*, path: Path, content: str, filename=False):
    global MAX_LINE_IN_METADA_FILE
    mkdir_if_not_exists(path)
    filename = filename if filename else str(get_latest_filename(path))
    fullpath = path.joinpath(filename)

    if fullpath.exists():
        with open(fullpath, 'r') as f:
            if(sum(1 for _ in f) >= MAX_LINE_IN_METADA_FILE):
                return record_metadata(path=path, filename=str(int(filename)+1), content=content)
    with open(fullpath, 'a+') as f:
        f.write(content)


def record_content(*, path: Path, filename: str, content: str):
    mkdir_if_not_exists(path)
    with open(path.joinpath(filename), 'w') as f:
        f.write(content)


def recieveEmail(emailAdressPool, path: Path):
    INDEX_SPLIT = 3

    email = generateSimpleEmail(emailAdressPool)
    email_content_hash = str(abs(hash(email.subject + email.content)))
    date = datetime.fromtimestamp(email.timestamp / 1_000_000)

    (year, month, day) = (str(date.year), str(
        date.month).rjust(2, '0'), str(date.day).rjust(2, '0'))

    metadata_fullpath = path.joinpath('meta').joinpath(
        year).joinpath(month).joinpath(day)
    record_metadata(path=metadata_fullpath,
                    content=f"{email.sender} {email.reciever} {email.timestamp} {email_content_hash}\n")

    email_content_fullpath = path.joinpath(
        'content').joinpath(email_content_hash[:INDEX_SPLIT])
    record_content(path=email_content_fullpath,
                   filename=email_content_hash[INDEX_SPLIT:],
                   content=f"{email.subject}\n\n{email.content}")


if __name__ == "__main__":
    # Set up
    DATA_PATH = Path("./data")
    emails = generateEmailAdresses(50)

    # Generate Emails
    while True:
        sleep(0.0001)
        recieveEmail(emails, DATA_PATH)
