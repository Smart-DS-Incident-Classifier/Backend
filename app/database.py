from pymongo import MongoClient
from app.config import settings

def get_database():
    client = MongoClient(settings.mongo_uri)
    db = client[settings.database_name]
    return db
