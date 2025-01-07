from fastapi import FastAPI
from app.routers import logs
from app.config import settings
from app.services.kafka_consumer import consume_logs
import asyncio

app = FastAPI(
    title="Log Ingestion API",
    description="An API for managing distributed system logs.",
    version="1.0.0",
)

@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, consume_logs, "log_data")

# Include routers
app.include_router(logs.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
