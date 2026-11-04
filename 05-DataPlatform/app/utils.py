#This utility will:
#- Generate UTC timestamps.
#- Configure application logging.
#- Append JSON records to files.
#- Create directories automatically.

import json
import os
import logging

from datetime import datetime, timezone
from pathlib import Path

from faker import Faker

fake = Faker()

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("data-generator")


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def write_jsonl(directory, filename, records):

    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)

    file_path = path / filename

    with file_path.open("a", encoding="utf-8") as file:

        for record in records:
            file.write(
                json.dumps(record, ensure_ascii=False) + "\n"
            )

    return file_path
