import time
import os
import json
from pathlib import Path
from typing import List
from .fakeEmails import Email
from ..batch import BatchLayer


class Receiver:
    DATA_PATH = Path('./data')

    def __init__(self):
        self.batchLayer = BatchLayer()

    def _get_emails_in_file(self, filepath: Path) -> List[dict]:
        print(f"Reading {filepath}")
        with open(filepath) as f:
            body = f.read()
            return json.loads(body)

    def process_emails_file(self, filepath):
        emails = self._get_emails_in_file(filepath)
        for email in emails:
            self.batchLayer.process_email(email)

    def run(self):
        while True:
            files = os.listdir(Receiver.DATA_PATH)
            files.sort(key=lambda f: os.path.getctime(
                Receiver.DATA_PATH.joinpath(f)))

            if len(files) > 1:
                for file in files:
                    # next_file = min(files, key=lambda filename: os.path.getctime(
                    #    Receiver.DATA_PATH.joinpath(filename)))
                    filepath = Receiver.DATA_PATH.joinpath(file)
                    self.process_emails_file(filepath)
                    os.remove(filepath)
            else:
                # Wait for new files to come
                print("Sleeping...")
                time.sleep(0.5)


if __name__ == "__main__":
    receiver = Receiver()
    receiver.run()
