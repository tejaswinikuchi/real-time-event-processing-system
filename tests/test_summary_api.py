from datetime import datetime
from app.models.processed_event import ProcessedEvent
from app.models.db import SessionLocal


def test_summary_endpoint(client):
    db = SessionLocal()

    db.add_all([
        ProcessedEvent(
            sensor_id="sensor-3",
            timestamp=datetime.utcnow(),
            value=10,
            type="temp"
        ),
        ProcessedEvent(
            sensor_id="sensor-3",
            timestamp=datetime.utcnow(),
            value=20,
            type="temp"
        ),
    ])

    db.commit()
    db.close()

    response = client.get("/api/events/summary/sensor-3")

    assert response.status_code == 200

    body = response.json()
    assert body["average"] == 15
    assert body["min"] == 10
    assert body["max"] == 20
