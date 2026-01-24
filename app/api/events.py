from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models.db import get_db
from app.models.processed_event import ProcessedEvent
from app.schemas.sensor_event import SensorReadingEvent
from app.kafka.producer import send_event_to_kafka
from app.cache.redis_client import get_cache, set_cache

# ✅ router owns /events
router = APIRouter(prefix="/events", tags=["Events"])


@router.post("", status_code=201)
def ingest_event(event: SensorReadingEvent):
    send_event_to_kafka(event.model_dump(mode="json"))
    return {"message": "Event sent successfully"}


@router.get("/{sensor_id}")
def get_events(sensor_id: str, db: Session = Depends(get_db)):
    cache_key = f"events:{sensor_id}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    events = (
        db.query(ProcessedEvent)
        .filter(ProcessedEvent.sensor_id == sensor_id)
        .order_by(ProcessedEvent.timestamp)
        .all()
    )

    if not events:
        raise HTTPException(status_code=404, detail="No events found")

    result = [
        {
            "id": e.id,
            "sensorId": e.sensor_id,
            "timestamp": e.timestamp.isoformat(),
            "value": e.value,
            "type": e.type,
        }
        for e in events
    ]

    set_cache(cache_key, result, 600)
    return result


@router.get("/summary/{sensor_id}")
def get_summary(sensor_id: str, db: Session = Depends(get_db)):
    cache_key = f"summary:{sensor_id}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    since = datetime.utcnow() - timedelta(hours=24)

    events = (
        db.query(ProcessedEvent)
        .filter(
            ProcessedEvent.sensor_id == sensor_id,
            ProcessedEvent.timestamp >= since
        )
        .all()
    )

    if not events:
        raise HTTPException(status_code=404, detail="No events found")

    values = [e.value for e in events]

    result = {
        "sensorId": sensor_id,
        "average": sum(values) / len(values),
        "min": min(values),
        "max": max(values),
    }

    set_cache(cache_key, result, 120)
    return result
