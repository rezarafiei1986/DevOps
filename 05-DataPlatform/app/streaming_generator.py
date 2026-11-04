#all streaming events share a common structure, while attributes contains event-specific information.

#This is useful for Spark because we can parse one common schema and then process individual event types.

import random
import time
import uuid
from app.kafka_producer import publish_batch
from app.config import KEEP_LOCAL_FILES

from faker import Faker

from app.config import (
    OUTPUT_DIR,
    STREAMING_BATCH_SIZE,
    STREAMING_INTERVAL_SECONDS
)

from app.utils import (
    utc_now,
    write_jsonl,
    logger
)

fake = Faker()

EVENT_TYPES = [
    "transaction",
    "page_view",
    "product_view",
    "login",
    "sensor_reading"
]


def generate_event():

    event_type = random.choice(EVENT_TYPES)

    event = {
        "event_id": str(uuid.uuid4()),
        "event_type": event_type,
        "user_id": random.randint(1, 1000),
        "session_id": str(uuid.uuid4()),
        "event_time": utc_now(),
        "source": "python-simulator",
        "attributes": {}
    }

    if event_type == "transaction":
        event["attributes"] = {
            "amount": round(random.uniform(5, 1000), 2),
            "currency": random.choice(["USD", "EUR", "GBP"]),
            "status": random.choice([
                "completed", "pending", "failed"
            ])
        }

    elif event_type == "page_view":
        event["attributes"] = {
            "page": random.choice([
                "/home", "/products", "/checkout", "/profile"
            ]),
            "duration_seconds": random.randint(1, 300)
        }

    elif event_type == "product_view":
        event["attributes"] = {
            "product_id": random.randint(1, 500),
            "category": random.choice([
                "electronics", "clothing", "books", "home"
            ])
        }

    elif event_type == "login":
        event["attributes"] = {
            "login_method": random.choice([
                "password", "google", "github"
            ]),
            "success": random.choice([True, True, True, False])
        }

    elif event_type == "sensor_reading":
        event["attributes"] = {
            "sensor_id": random.randint(1, 50),
            "temperature": round(random.uniform(15, 40), 2),
            "humidity": round(random.uniform(20, 90), 2)
        }

    return event



def run_streaming_generator(stop_event):

    logger.info("Streaming generator started")

    while not stop_event.is_set():

        # 1. Generate streaming events
        records = [
            generate_event()
            for _ in range(STREAMING_BATCH_SIZE)
        ]

        # 2. Save locally for debugging
        if KEEP_LOCAL_FILES:

            file_path = write_jsonl(
                f"{OUTPUT_DIR}/streaming",
                "streaming-events.jsonl",
                records
            )

            logger.info(
                "Saved %s streaming events locally | file=%s",
                len(records),
                file_path
            )

        # 3. Publish events to Kafka
        publish_batch(
            topic="streaming-events",
            records=records,
            key_field="user_id"
        )

        logger.info(
            "Generated and published %s streaming events",
            len(records)
        )

        # 4. Wait before generating the next batch
        stop_event.wait(
            STREAMING_INTERVAL_SECONDS
        )

    logger.info("Streaming generator stopped")
