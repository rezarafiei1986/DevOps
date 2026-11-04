#separating customers, products, and orders into different files. Later, this makes it straightforward to create three Kafka topics and three corresponding Iceberg tables.import random
import random
import uuid

from app.kafka_producer import publish_batch

from app.config import KEEP_LOCAL_FILES

from faker import Faker

from app.config import (
    OUTPUT_DIR,
    RAW_BATCH_SIZE,
    RAW_BATCH_INTERVAL_SECONDS
)

from app.utils import (
    utc_now,
    write_jsonl,
    logger
)

fake = Faker()

CUSTOMER_IDS = []
PRODUCT_IDS = []


def generate_customer():

    customer_id = str(uuid.uuid4())

    CUSTOMER_IDS.append(customer_id)

    return {
        "record_id": customer_id,
        "record_type": "customer",
        "name": fake.name(),
        "email": fake.email(),
        "country": fake.country(),
        "city": fake.city(),
        "created_at": utc_now()
    }


def generate_product():

    product_id = str(uuid.uuid4())

    PRODUCT_IDS.append(product_id)

    return {
        "record_id": product_id,
        "record_type": "product",
        "product_name": fake.catch_phrase(),
        "category": random.choice([
            "electronics",
            "clothing",
            "books",
            "home"
        ]),
        "price": round(random.uniform(5, 2000), 2),
        "created_at": utc_now()
    }


def generate_order():

    return {
        "record_id": str(uuid.uuid4()),
        "record_type": "order",
        "customer_id": random.choice(CUSTOMER_IDS),
        "product_id": random.choice(PRODUCT_IDS),
        "quantity": random.randint(1, 5),
        "total_amount": round(random.uniform(10, 3000), 2),
        "status": random.choice([
            "created",
            "paid",
            "shipped",
            "cancelled"
        ]),
        "created_at": utc_now()
    }

def run_raw_generator(stop_event):

    logger.info("Raw data generator started")

    while not stop_event.is_set():

        # 1. Generate customers
        customers = [
            generate_customer()
            for _ in range(5)
        ]

        # 2. Generate products
        products = [
            generate_product()
            for _ in range(5)
        ]

        # 3. Generate orders
        orders = [
            generate_order()
            for _ in range(RAW_BATCH_SIZE)
        ]

        # 4. Save locally for debugging
        if KEEP_LOCAL_FILES:

            write_jsonl(
                f"{OUTPUT_DIR}/raw",
                "customers.jsonl",
                customers
            )

            write_jsonl(
                f"{OUTPUT_DIR}/raw",
                "products.jsonl",
                products
            )

            write_jsonl(
                f"{OUTPUT_DIR}/raw",
                "orders.jsonl",
                orders
            )

        # 5. Publish customers to Kafka
        publish_batch(
            topic="raw-customers",
            records=customers
        )

        # 6. Publish products to Kafka
        publish_batch(
            topic="raw-products",
            records=products
        )

        # 7. Publish orders to Kafka
        publish_batch(
            topic="raw-orders",
            records=orders
        )

        # 8. Log batch summary
        logger.info(
            "Generated and published customers=%s products=%s orders=%s",
            len(customers),
            len(products),
            len(orders)
        )

        # 9. Wait before next batch
        stop_event.wait(
            RAW_BATCH_INTERVAL_SECONDS
        )

    logger.info("Raw data generator stopped")
