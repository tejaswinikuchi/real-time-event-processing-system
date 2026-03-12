from fastapi import FastAPI
from sqlalchemy.exc import OperationalError
import time

from app.config.database import engine
from app.models.processed_event import Base
from app.api import events

app = FastAPI()

# Retry DB connection
MAX_RETRIES = 10
RETRY_DELAY = 3

for attempt in range(MAX_RETRIES):
    try:
        Base.metadata.create_all(bind=engine)
        print("Database connected and tables created")
        break
    except OperationalError:
        print(f"Database not ready, retrying... ({attempt+1}/{MAX_RETRIES})")
        time.sleep(RETRY_DELAY)
else:
    raise Exception("Could not connect to database")

# IMPORTANT: no prefix here
app.include_router(events.router)