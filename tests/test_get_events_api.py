from datetime import datetime
from app.models.processed_event import ProcessedEvent
from app.models.db import SessionLocal


def test_get_events_by_sensor(client):
    db = SessionLocal()

    event = ProcessedEvent(
        sensor_id="sensor-2",
        timestamp=datetime.utcnow(),
        value=30.5,
        type="temperature"
    )

    db.add(event)
    db.commit()
    db.close()

    response = client.get("/api/events/sensor-2")

    assert response.status_code == 200
    assert len(response.json()) == 1
