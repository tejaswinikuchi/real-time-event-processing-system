from sqlalchemy.orm import Session
from app.models.event import Event

def get_all_events(db: Session):
    return db.query(Event).order_by(Event.timestamp.desc()).all()
