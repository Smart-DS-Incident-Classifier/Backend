from fastapi import APIRouter, HTTPException, Depends
from app.models.model import Log
from app.services.service import add_log, fetch_logs, delete_logs

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
