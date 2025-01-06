from pydantic import BaseModel, Field
from datetime import datetime

class Log(BaseModel):
    source: str = Field(..., description="Source of the log (e.g., Hadoop, HDFS)")
    severity: str = Field(..., description="Severity level (e.g., High, Medium, Low)")
    message: str = Field(..., description="Log message")
    timestamp: str = Field(..., description="Timestamp in ISO 8601 format")

    @classmethod
    def validate_timestamp(cls, value: str) -> str:
        try:
            datetime.fromisoformat(value)
            return value
        except ValueError:
            raise ValueError("Invalid timestamp format")
