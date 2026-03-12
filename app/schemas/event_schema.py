from pydantic import BaseModel
from datetime import datetime


class EventCreate(BaseModel):
    sensorId: str
    timestamp: datetime
    value: float
    type: str