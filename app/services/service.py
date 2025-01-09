from app.database import get_database
from app.config import settings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def add_log(log: dict):
    db = get_database()
    collection = db[settings.database_name]
    collection.insert_one(log)
    return {"message": "Log added successfully"}

def fetch_logs(query: dict = {}): #get all logs from db {} is the filter is na then get all
    db = get_database()
    collection = db[settings.database_name]
    return list(collection.find(query, {"_id": 0}))

def delete_logs(query: dict):
    db = get_database()
    collection = db[settings.database_name]
    result = collection.delete_many(query)
    return {"deleted_count": result.deleted_count}

def find_similar_incidents(message: str):
    logs = fetch_logs()
    if not logs:
        return None

    historical_messages = [logs["message"] for logs in logs]
    all_messages = historical_messages + [message]

    #use TF-IDF vectors
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_messages)

    #calculate consine similarity between new message and historical message; first and last
    similarities = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1])

    #find the most similar historical incident
    max_sim_index = np.argmax(similarities[0])
    max_sim_score = similarities[0][max_sim_index]

    if max_sim_score > 0.5:
        return {
            "historical_logs" : logs[max_sim_index],
            "similarity_score": max_sim_score
        }
    return None

