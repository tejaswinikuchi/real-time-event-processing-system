import uuid
from datetime import datetime

from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.sql import func

from app.models.db import Base


class ProcessedEvent(Base):
    __tablename__ = "processed_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    sensor_id = Column(String(50), index=True, nullable=False)

    timestamp = Column(DateTime, nullable=False)

    value = Column(Float, nullable=False)

    type = Column(String(50), nullable=False)

    processed_at = Column(DateTime, server_default=func.now())