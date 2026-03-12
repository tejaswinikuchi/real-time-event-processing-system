from datetime import datetime
from app.models.db import SessionLocal
from app.models.processed_event import ProcessedEvent


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

    response = client.get("/events/summary/sensor-3")

    assert response.status_code == 200

    data = response.json()

    assert data["min"] == 10
    assert data["max"] == 20