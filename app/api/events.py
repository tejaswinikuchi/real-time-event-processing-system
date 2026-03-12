from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.config.settings import settings
from app.schemas.event_schema import EventCreate
from app.models.processed_event import ProcessedEvent
from app.kafka.producer import send_event_to_kafka
from app.cache.redis_client import get_cache, set_cache

router = APIRouter()


@router.post("/events", status_code=status.HTTP_201_CREATED)
def create_event(event: EventCreate):

    payload = event.model_dump()

    payload["timestamp"] = str(payload["timestamp"])

    send_event_to_kafka(payload)

    return {"message": "Event sent to Kafka"}


@router.get("/events/{sensor_id}")
def get_events(sensor_id: str):

    cache_key = f"events:{sensor_id}"

    # Check cache first
    cached_data = get_cache(cache_key)
    if cached_data:
        return cached_data

    db: Session = SessionLocal()

    events = (
        db.query(ProcessedEvent)
        .filter(ProcessedEvent.sensor_id == sensor_id)
        .order_by(ProcessedEvent.timestamp)
        .all()
    )

    db.close()

    if not events:
        raise HTTPException(status_code=404, detail="No events found")

    result = [
        {
            "sensorId": e.sensor_id,
            "timestamp": e.timestamp.isoformat(),
            "value": e.value,
            "type": e.type
        }
        for e in events
    ]

    # Store in cache using env TTL
    set_cache(cache_key, result, settings.EVENTS_CACHE_TTL)

    return result


@router.get("/events/summary/{sensor_id}")
def get_summary(sensor_id: str):

    cache_key = f"summary:{sensor_id}"

    # Check cache first
    cached_data = get_cache(cache_key)
    if cached_data:
        return cached_data

    db: Session = SessionLocal()

    events = (
        db.query(ProcessedEvent)
        .filter(ProcessedEvent.sensor_id == sensor_id)
        .all()
    )

    db.close()

    if not events:
        raise HTTPException(status_code=404, detail="No data found")

    values = [e.value for e in events]

    result = {
        "average": sum(values) / len(values),
        "min": min(values),
        "max": max(values)
    }

    # Store in cache using env TTL
    set_cache(cache_key, result, settings.SUMMARY_CACHE_TTL)

    return result