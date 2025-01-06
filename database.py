from pymongo import MongoClient


def get_database():
    # Replace <password> with your MongoDB password
    connection_string = "mongodb+srv://admin:admin@cluster0.yxrab4v.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    # Connect to MongoDB
    client = MongoClient(connection_string)

    # Access the database
    db = client["distrubutedSystemDB"]
    return db


def get_collection():
    # Access the database
    db = get_database()

    # Access the collection within the database
    collection = db["distrubutedSystemDB"]
    return collection
