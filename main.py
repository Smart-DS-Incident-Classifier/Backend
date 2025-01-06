from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from database import get_database

app = FastAPI()


# Pydantic model for log validation
class Log(BaseModel):
    source: str = Field(..., description="Source of the log (e.g., Hadoop, HDFS)")
    severity: str = Field(..., description="Severity level (e.g., High, Medium, Low)")
    message: str = Field(..., description="Log message")
    timestamp: str = Field(..., description="Timestamp in ISO 8601 format")


@app.post("/logs/upload")
async def upload_log(log: Log):
    try:
        # Validate timestamp format
        datetime.fromisoformat(log.timestamp)

        # Save log to database
        db = get_database()
        db.logs.insert_one(log.dict())

        return {"message": "Log uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/logs/")
async def fetch_logs(severity: Optional[str] = None):
    db = get_database()

    query = {}
    if severity:
        query["severity"] = severity

    logs = list(db.logs.find(query, {"_id": 0}))
    return {"logs": logs}


