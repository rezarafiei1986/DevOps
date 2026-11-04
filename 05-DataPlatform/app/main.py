#This starts both generators independently. If you stop the container, both generators receive a shutdown signal.


import threading
import signal

from app.config import GENERATOR_MODE
from app.streaming_generator import run_streaming_generator
from app.raw_generator import run_raw_generator

from app.utils import logger

from app.kafka_producer import flush_producer


stop_event = threading.Event()


def shutdown_handler(signum, frame):

    logger.info("Shutdown signal received")

    stop_event.set()


def main():

    signal.signal(signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGINT, shutdown_handler)

    logger.info("Starting Python Data Generator")
    logger.info("Mode: %s", GENERATOR_MODE)

    generators = {
        "streaming": run_streaming_generator,
        "raw": run_raw_generator
    }

    if GENERATOR_MODE == "both":
        selected = ["streaming", "raw"]

    elif GENERATOR_MODE in generators:
        selected = [GENERATOR_MODE]

    else:
        raise ValueError(
            f"Invalid GENERATOR_MODE: {GENERATOR_MODE}"
        )

    threads = []

    for name in selected:

        thread = threading.Thread(
            target=generators[name],
            args=(stop_event,),
            name=name,
            daemon=False
        )

        threads.append(thread)
        thread.start()

    try:

        while any(thread.is_alive() for thread in threads):
            for thread in threads:
                thread.join(timeout=1)

    except KeyboardInterrupt:

        stop_event.set()

    finally:

        stop_event.set()

        for thread in threads:
            thread.join()

        # Flush pending Kafka messages before exiting
        flush_producer()


        logger.info("Data Generator stopped")


if __name__ == "__main__":
    main()
