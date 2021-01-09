import os
import json
import time
from pathlib import Path
from datetime import datetime
from fakeEmails import Email, generateEmailAdresses, generateEmails

DATA_PATH = Path("./data")
CHUNK_AMOUNT_LIMIT = 100
EMAIL_ADRESS_AMOUNT = 100
EMAIL_IN_CHUNK = 250
SPAM_RATE = 0.1
FLOOD_RATE_PER_CHUNK = 0.1
SLEEP_TIME_IN_S = 1


def run():

    def mkdir_if_not_exists(path: Path):
        if not path.exists():
            path.mkdir(parents=True)

    def get_latest_filename(path: Path) -> int:
        return max(1, len(os.listdir(path)))

    def waitIfFileChunkLimitReached(path: Path, limit: int, sleep_time: int):
        while True:
            file_in_queue = len(os.listdir(DATA_PATH))

            if file_in_queue >= limit:
                print('Sleeping...')
                time.sleep(sleep_time)
            else:
                return

    def toDict(x): return x.__dict__

    # Set up
    emailsAdresses = generateEmailAdresses(EMAIL_ADRESS_AMOUNT)
    mkdir_if_not_exists(DATA_PATH)

    # Main
    email_chunk = get_latest_filename(DATA_PATH)
    # Check tout les 1000 fichiers → si 5000 alors pause; puis recheck, si correct → generate email
    while True:
        waitIfFileChunkLimitReached(
            DATA_PATH, CHUNK_AMOUNT_LIMIT, SLEEP_TIME_IN_S)

        startTime = time.time()
        filepath = DATA_PATH.joinpath(str(email_chunk))
        emails = list(map(toDict, generateEmails(emailsAdresses, spam_rate=SPAM_RATE,
                                                 flood_rate=FLOOD_RATE_PER_CHUNK, email_amount=EMAIL_IN_CHUNK)))

        with open(filepath, 'w') as f:
            json.dump(emails, f, indent=2)

        print(f'{email_chunk} in {time.time() - startTime}')
        email_chunk += 1


if __name__ == "__main__":
    run()
