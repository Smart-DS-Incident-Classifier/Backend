from fastapi import APIRouter, HTTPException, Depends
from app.models.model import Log
from app.services.service import add_log, fetch_logs, delete_logs
from app.services.kafka_producer import produce_log

router = APIRouter(prefix="/logs", tags=["Logs"])

@router.post("/upload")
async def upload_log(log: Log):
    try:
        add_log(log.dict())
        return {"message": "Log uploaded successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def get_logs(severity: str = None):
    query = {"severity": severity} if severity else {}
    logs = fetch_logs(query)
    return {"logs": logs}

@router.delete("/")
async def remove_logs(severity: str):
    query = {"severity": severity}
    result = delete_logs(query)
    return result

@router.post("/stream")
async def stream_log(log: Log):
    try:
        log_data = log.dict()
        produce_log("logs_topic", log_data)  # Replace "logs_topic" with your Kafka topic
        return {"message": "Log streamed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to stream log: {e}")
