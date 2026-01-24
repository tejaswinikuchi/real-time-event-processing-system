import os
from dotenv import load_dotenv

load_dotenv()  # THIS IS VERY IMPORTANT

class Settings:
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "events_db")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "root")

    MYSQL_URL = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
        f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    )

    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "")
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "sensor_readings")

    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

    EVENTS_CACHE_TTL = int(os.getenv("EVENTS_CACHE_TTL", 600))
    SUMMARY_CACHE_TTL = int(os.getenv("SUMMARY_CACHE_TTL", 120))

settings = Settings()
