from datetime import datetime
from app.models.db import SessionLocal
from app.models.processed_event import ProcessedEvent


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

    response = client.get("/events/sensor-2")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert data[0]["sensorId"] == "sensor-2"