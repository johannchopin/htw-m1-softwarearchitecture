import os
from pathlib import Path
from datetime import datetime
from time import sleep
from fakeEmails import Email, generateEmailAdresses, generateSimpleEmail, getTimestamp


def _mkdir_if_not_exists(path: Path):
    if not path.exists():
        path.mkdir(parents=True)


def _get_latest_filename(path: Path) -> int:
    return len(os.listdir(path))

    INDEX_SPLIT = 3

    email = generateSimpleEmail(emailAdressPool)
    email_content_hash = str(abs(hash(email.subject + email.content)))
    date = datetime.fromtimestamp(email.timestamp / 1_000_000)

    (year, month, day) = (str(date.year), str(
        date.month).rjust(2, '0'), str(date.day).rjust(2, '0'))

    metadata_fullpath = path.joinpath('meta').joinpath(
        year).joinpath(month).joinpath(day)
    save_content_in_file(path=metadata_fullpath,
                         filename=_get_latest_filename(metadata_fullpath),
                         content=f"{email.sender} {email.reciever} {email.timestamp} {email_content_hash}\n")

    email_content_fullpath = path.joinpath(
        'content').joinpath(email_content_hash[:INDEX_SPLIT])
    save_content_in_file(path=email_content_fullpath,
                         filename=email_content_hash[INDEX_SPLIT:],
                         content=f"{email.subject}\n\n{email.content}",
                         check_file_size=False)


if __name__ == "__main__":
    # Set up
    DATA_PATH = Path("./data")
    emails = generateEmailAdresses(50)

    # Generate Emails
    while True:
        sleep(0.1)
        recieveEmail(emails, DATA_PATH)
