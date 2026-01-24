import time
import logging
from fastapi import FastAPI

from app.api.events import router as events_router
from app.models.db import Base, engine

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Real-Time Event Processing System")

#  Only /api here
app.include_router(events_router, prefix="/api")


@app.on_event("startup")
def startup_event():
    retries = 10
    delay = 3

    for attempt in range(retries):
        try:
            logging.info("Attempting database connection...")
            Base.metadata.create_all(bind=engine)
            logging.info("Database ready")
            break
        except Exception as e:
            logging.error(f"Database not ready ({attempt+1}/{retries}): {e}")
            time.sleep(delay)
    else:
        logging.critical("Database never became ready. Exiting.")
        raise RuntimeError("Database unavailable")
