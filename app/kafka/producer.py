import json
import logging
from kafka import KafkaProducer
from kafka.errors import KafkaError

from app.config.settings import settings

logger = logging.getLogger(__name__)

producer = KafkaProducer(
    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)


def send_event_to_kafka(event: dict):
    """
    Send event to Kafka safely.
    Prevent API crash if Kafka is unavailable.
    """

    try:
        producer.send(settings.KAFKA_TOPIC, event)
        producer.flush()

    except KafkaError as e:
        logger.error("Kafka producer error: %s", str(e))

        # Do NOT crash API
        # just log and continue

    except Exception as e:
        logger.error("Unexpected producer error: %s", str(e))