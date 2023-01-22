from datetime import datetime

from pydantic import BaseModel, Field


class TimePeriod(BaseModel):
    startTime: datetime = Field(..., description="Start time of the class")
    duration: float = Field(..., description="Duration of the class")
    weekDay: int = Field(..., description="Weekday of the class")
