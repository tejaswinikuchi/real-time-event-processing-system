from pydantic import BaseModel, Field
from datetime import datetime


class SensorReadingEvent(BaseModel):
    sensorId: str = Field(..., min_length=1)
    timestamp: datetime
    value: float
    type: str = Field(..., min_length=1)

    class Config:
        json_schema_extra = {
            "example": {
                "sensorId": "sensor-1",
                "timestamp": "2026-01-23T10:00:00Z",
                "value": 28.4,
                "type": "temperature"
            }
        }
