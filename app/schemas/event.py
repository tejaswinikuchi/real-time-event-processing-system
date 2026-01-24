from datetime import datetime
from pydantic import BaseModel

class EventResponse(BaseModel):
    id: int
    sensor_id: str
    event_type: str
    value: float
    timestamp: datetime

    class Config:
        from_attributes = True
