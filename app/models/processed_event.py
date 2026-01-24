from sqlalchemy import Column, String, DateTime, Float
from datetime import datetime
from app.models.db import Base


class ProcessedEvent(Base):
    __tablename__ = "processed_events"

    id = Column(String(36), primary_key=True, index=True)
    sensor_id = Column(String(255), index=True, nullable=False)
    timestamp = Column(DateTime, index=True, nullable=False)
    value = Column(Float, nullable=False)
    type = Column(String(100), nullable=False)
    processed_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
