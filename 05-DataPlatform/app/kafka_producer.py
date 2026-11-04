import json
import os

from confluent_kafka import Producer

from app.utils import logger


KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "kafka:9092"
)

ENABLE_KAFKA = os.getenv(
    "ENABLE_KAFKA", "true"
).lower() == "true"


producer = None


def get_producer():

    global producer

    if not ENABLE_KAFKA:
        return None

    if producer is None:

        producer = Producer({
            "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
            "client.id": "python-data-generator",
            "acks": "all",
            "enable.idempotence": True,
            "retries": 10
        })

        logger.info(
            "Kafka producer initialized: %s",
            KAFKA_BOOTSTRAP_SERVERS
        )

    return producer


def delivery_report(err, msg):

    if err is not None:

        logger.error(
            "Kafka delivery failed: %s",
            err
        )

    else:

        logger.debug(
            "Kafka delivered topic=%s partition=%s offset=%s",
            msg.topic(),
            msg.partition(),
            msg.offset()
        )


def publish_batch(topic, records, key_field="record_id"):

    kafka = get_producer()

    if kafka is None:
        return

    for record in records:

        key = str(record.get(key_field, ""))

        value = json.dumps(
            record,
            ensure_ascii=False
        )

        kafka.produce(
            topic=topic,
            key=key,
            value=value,
            callback=delivery_report
        )

        kafka.poll(0)

    remaining = kafka.flush(10)

    if remaining:
        logger.warning(
            "%s messages remain undelivered for topic %s",
            remaining,
            topic
        )

    else:
        logger.info(
            "Published %s messages to Kafka topic=%s",
            len(records),
            topic
        )


def flush_producer():

    if producer is not None:

        remaining = producer.flush(10)

        logger.info(
            "Kafka producer shutdown. Pending messages: %s",
            remaining
        )
