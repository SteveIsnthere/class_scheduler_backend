from pydantic import BaseModel, Field
from datetime import datetime


class TimePeriod(BaseModel):
    startTime: datetime = Field(..., description="Start time of the class")
    duration: float = Field(..., description="Duration of the class")
    weekDay: int = Field(..., description="Weekday of the class")
