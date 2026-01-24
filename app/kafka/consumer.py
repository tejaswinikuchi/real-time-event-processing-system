import json
import logging
import time
import uuid
from datetime import datetime

from kafka import KafkaConsumer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.db import SessionLocal
from app.models.processed_event import ProcessedEvent
from app.cache.redis_client import delete_cache

logging.basicConfig(level=logging.INFO)

KAFKA_TOPIC = "sensor_readings"


def consume_events():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=["kafka:9092"],
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="event-processing-group",
    )

    logging.info("Kafka consumer started. Waiting for messages...")

    for message in consumer:
        event = message.value
        db: Session = SessionLocal()

        try:
            processed_event = ProcessedEvent(
                id=str(uuid.uuid4()),  # idempotency handled by PK
                sensor_id=event["sensorId"],
                timestamp=datetime.fromisoformat(
                    event["timestamp"].replace("Z", "")
                ),
                value=event["value"],
                type=event["type"],
            )

            db.add(processed_event)
            db.commit()

            # 🔥 CACHE INVALIDATION (THIS IS THE KEY FIX)
            delete_cache(f"events:{event['sensorId']}")
            delete_cache(f"summary:{event['sensorId']}")

            logging.info(
                f"Processed event for sensor {event['sensorId']}"
            )

        except IntegrityError:
            # Duplicate message → safe to ignore
            db.rollback()
            logging.warning("Duplicate event ignored (idempotent handling)")

        except Exception as e:
            db.rollback()
            logging.error(f"Error processing event: {e}")

        finally:
            db.close()


if __name__ == "__main__":
    # Small delay to allow Kafka & DB to be ready
    time.sleep(10)
    consume_events()
