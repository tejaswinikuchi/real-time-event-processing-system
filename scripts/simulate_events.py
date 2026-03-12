import requests
import random
import time
from datetime import datetime, timezone

API_URL = "http://localhost:8080/events"

SENSOR_IDS = ["sensor-1", "sensor-2", "sensor-3"]
EVENT_TYPES = ["temperature", "humidity", "pressure"]


def generate_event():
    return {
        "sensorId": random.choice(SENSOR_IDS),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "value": round(random.uniform(10, 40), 2),
        "type": random.choice(EVENT_TYPES),
    }


def send_event():
    event = generate_event()
    response = requests.post(API_URL, json=event)

    print("Sent:", event)
    print("Response:", response.status_code, response.text)
    print("-" * 40)


if __name__ == "__main__":
    print("Starting event simulation...\n")

    for _ in range(20):
        send_event()
        time.sleep(1)

    print("\nSimulation finished.")