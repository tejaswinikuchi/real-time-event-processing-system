import json
import uuid
import logging
from datetime import datetime

from kafka import KafkaConsumer
from sqlalchemy.exc import IntegrityError

from app.config.settings import settings
from app.config.database import SessionLocal
from app.models.processed_event import ProcessedEvent
from app.cache.redis_client import delete_cache

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


consumer = KafkaConsumer(
    settings.KAFKA_TOPIC,
    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="event-processing-group"
)


def process_event(event: dict):
    """
    Process Kafka event and store in database.
    Implements idempotent processing.
    """

    db = SessionLocal()

    try:

        processed_event = ProcessedEvent(
            id=str(uuid.uuid4()),
            sensor_id=event["sensorId"],
            timestamp=datetime.fromisoformat(event["timestamp"]),
            value=event["value"],
            type=event["type"],
            processed_at=datetime.utcnow()
        )

        db.add(processed_event)
        db.commit()

        # Invalidate Redis caches
        delete_cache(f"events:{event['sensorId']}")
        delete_cache(f"summary:{event['sensorId']}")

        logger.info("Processed event for sensor %s", event["sensorId"])

    except IntegrityError:
        db.rollback()
        logger.warning("Duplicate event detected, skipping")

    except Exception as e:
        db.rollback()
        logger.error("Error processing event: %s", str(e))

    finally:
        db.close()


def consume_events():
    """
    Kafka consumer loop.
    Continuously consumes events and processes them.
    """

    logger.info("Kafka consumer started...")

    for message in consumer:
        try:

            event = message.value
            process_event(event)

        except Exception as e:
            logger.error("Consumer error: %s", str(e))


if __name__ == "__main__":
    consume_events()