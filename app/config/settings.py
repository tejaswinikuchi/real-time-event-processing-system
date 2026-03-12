from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DATABASE_URL: str

    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_TOPIC: str

    REDIS_HOST: str
    REDIS_PORT: int

    EVENTS_CACHE_TTL: int
    SUMMARY_CACHE_TTL: int

    class Config:
        env_file = ".env"


settings = Settings()