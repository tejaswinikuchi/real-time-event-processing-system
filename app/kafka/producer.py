import os
import json
import logging
from datetime import datetime
from confluent_kafka import Producer

logger = logging.getLogger(__name__)

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TOPIC_NAME = os.getenv("KAFKA_TOPIC", "sensor_readings")

# Detect test environment
IS_TESTING = os.getenv("TESTING", "false").lower() == "true"

producer_config = {
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
    "linger.ms": 5,
}

producer = Producer(producer_config)


def _json_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def send_event_to_kafka(event: dict):
    """
    Non-blocking Kafka producer.
    Safe for tests and production.
    """
    if IS_TESTING:
        # Do NOTHING in tests
        return

    try:
        producer.produce(
            topic=TOPIC_NAME,
            value=json.dumps(event, default=_json_serializer)
        )
        producer.poll(0)  #  NON-BLOCKING
    except Exception as e:
        logger.error(f"Kafka produce failed: {e}")
        raise
