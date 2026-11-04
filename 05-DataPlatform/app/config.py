import os
from dotenv import load_dotenv

load_dotenv()

GENERATOR_MODE = os.getenv(
    "GENERATOR_MODE", "both"
)

STREAMING_INTERVAL_SECONDS = float(
    os.getenv("STREAMING_INTERVAL_SECONDS", "1")
)

STREAMING_BATCH_SIZE = int(
    os.getenv("STREAMING_BATCH_SIZE", "5")
)

RAW_BATCH_INTERVAL_SECONDS = float(
    os.getenv("RAW_BATCH_INTERVAL_SECONDS", "10")
)

RAW_BATCH_SIZE = int(
    os.getenv("RAW_BATCH_SIZE", "20")
)

OUTPUT_DIR = os.getenv(
    "OUTPUT_DIR", "/app/data"
)

LOG_LEVEL = os.getenv(
    "LOG_LEVEL", "INFO"
)


KEEP_LOCAL_FILES = os.getenv(
    "KEEP_LOCAL_FILES", "true"
).lower() == "true"
