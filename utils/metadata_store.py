import json
import os

METADATA_FILE = (
    "metadata/processed_files.json"
)

os.makedirs(
    "metadata",
    exist_ok=True
)


def load_metadata():

    if not os.path.exists(
        METADATA_FILE
    ):
        return {}

    with open(
        METADATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def save_metadata(
    metadata
):

    with open(
        METADATA_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metadata,
            file,
            indent=4
        )