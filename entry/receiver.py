import time
import os
from pathlib import Path


DATA_PATH = Path('./data')


def run():
    global DATA_PATH
    while True:
        files = os.listdir(DATA_PATH)

        if len(files):
            next_file = min(files, key=lambda filename: os.path.getctime(
                DATA_PATH.joinpath(filename)))
            print(f"Reading {next_file}")
            # TODO: Send to Batch and Serving Layer
            time.sleep(1)
            os.remove(DATA_PATH.joinpath(next_file))
        else:
            # Wait for new files to come
            print("Sleeping...")
            time.sleep(1)


if __name__ == "__main__":
    run()
