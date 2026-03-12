from fastapi.testclient import TestClient


def test_invalid_event_payload(client):
    response = client.post(
        "/events",
        json={
            "sensorId": "sensor-x",
            "value": 25.4,
            "type": "temperature"
        }
    )

    assert response.status_code == 422


def test_valid_event_payload(client, monkeypatch):

    def mock_send(*args, **kwargs):
        return None

    monkeypatch.setattr(
        "app.kafka.producer.send_event_to_kafka",
        mock_send
    )

    response = client.post(
        "/events",
        json={
            "sensorId": "sensor-1",
            "timestamp": "2026-01-23T10:00:00Z",
            "value": 28.4,
            "type": "temperature"
        }
    )

    assert response.status_code == 201