from datetime import datetime
from fastapi.testclient import TestClient

from app.main import app
from app.config.database import SessionLocal
from app.models.processed_event import ProcessedEvent

client = TestClient(app)


def seed_event(sensor_id):
    db = SessionLocal()

    event = ProcessedEvent(
        sensor_id=sensor_id,
        timestamp=datetime.utcnow(),
        value=25.5,
        type="temperature"
    )

    db.add(event)
    db.commit()
    db.close()


def test_event_pipeline_end_to_end():

    sensor_id = "integration-test-sensor"

    payload = {
        "sensorId": sensor_id,
        "timestamp": "2026-01-01T10:00:00",
        "value": 25.5,
        "type": "temperature"
    }

    response = client.post("/events", json=payload)

    assert response.status_code == 201


def test_get_events_endpoint():

    sensor_id = "integration-test-sensor"

    seed_event(sensor_id)

    response = client.get(f"/events/{sensor_id}")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert data[0]["sensorId"] == sensor_id


def test_summary_endpoint():

    sensor_id = "integration-test-sensor"

    seed_event(sensor_id)

    response = client.get(f"/events/summary/{sensor_id}")

    assert response.status_code == 200

    data = response.json()

    assert "average" in data
    assert "min" in data
    assert "max" in data