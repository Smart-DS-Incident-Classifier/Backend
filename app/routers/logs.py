from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from app.models.model import Log
from app.services.service import add_log, fetch_logs, delete_logs
from app.services.kafka_producer import produce_log
import csv
import json
from typing import List

router = APIRouter(prefix="/logs", tags=["Logs"])

def parse_csv(file: UploadFile) -> List[dict]:
    """Parse CSV log data."""
    try:
        content = file.file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(content)
        logs = [row for row in reader]
        return logs
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid CSV format: {e}")

def parse_plain_text(file: UploadFile) -> List[dict]:
    """Parse plain text log data."""
    try:
        content = file.file.read().decode("utf-8").splitlines()
        logs = [{"message": line.strip()} for line in content if line.strip()]
        return logs
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid plain text format: {e}")


@router.post("/upload")
async def upload_log(format: str, file: UploadFile = File(...)):
    """
    Ingest logs in JSON, CSV, or plain text format.
    - format: json, csv, or plain_text
    - file: Uploaded log file
    """
    try:
        if format == "json":
            data = json.loads(file.file.read().decode("utf-8"))
            logs = data if isinstance(data, list) else [data]
        elif format == "csv":
            logs = parse_csv(file)
        elif format == "plain_text":
            logs = parse_plain_text(file)
        else:
            raise HTTPException(status_code=400, detail="Unsupported format. Use 'json', 'csv', or 'plain_text'.")

        # Validate and add logs to the database
        for log in logs:
            if "message" not in log:
                raise HTTPException(status_code=400, detail=f"Log entry missing required 'message' field: {log}")
            add_log(log)

        return {"message": "Logs uploaded successfully!", "log_count": len(logs)}

    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON format: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading logs: {e}")

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
