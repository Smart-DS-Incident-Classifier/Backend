from fastapi import FastAPI
from app.routers import logs
from app.config import settings

app = FastAPI(
    title="Log Ingestion API",
    description="An API for managing distributed system logs.",
    version="1.0.0",
)

# Include routers
app.include_router(logs.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
