from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongo_uri: str
    database_name: str
    collection_name: str
    kafka_broker: str

    class Config:
        env_file = ".env"

settings = Settings()
