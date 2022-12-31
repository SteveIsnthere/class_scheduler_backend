from pydantic import BaseModel, Field
from datetime import datetime


class UnableTime(BaseModel):
    startTime: datetime = Field(..., description="Start time of the class")
    duration: float = Field(..., description="Duration of the class")
    isInconvenient: bool = Field(..., description="Whether the class is inconvenient")
    weekDay: int = Field(..., description="Weekday of the class")
