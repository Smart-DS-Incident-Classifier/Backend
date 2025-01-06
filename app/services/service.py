from app.database import get_database

def add_log(log: dict):
    db = get_database()
    collection = db["distrubutedSystemDB"]
    collection.insert_one(log)
    return {"message": "Log added successfully"}

def fetch_logs(query: dict = {}):
    db = get_database()
    collection = db["distrubutedSystemDB"]
    return list(collection.find(query, {"_id": 0}))

def delete_logs(query: dict):
    db = get_database()
    collection = db["distrubutedSystemDB"]
    result = collection.delete_many(query)
    return {"deleted_count": result.deleted_count}
