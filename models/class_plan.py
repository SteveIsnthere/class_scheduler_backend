from pydantic import BaseModel, Field
from datetime import datetime
from models.relation import Relation


class ClassPlan(BaseModel):
    weekDay: int = Field(..., description="Weekday of the class")
    info: Relation = Field(..., description="Info of the class")
    startTime: datetime = Field(..., description="Start time of the class")
    duration: float = Field(..., description="Duration of the class")
