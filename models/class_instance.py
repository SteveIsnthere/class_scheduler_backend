from datetime import datetime

from pydantic import BaseModel, Field

from models.relation import Relation


class ClassInstance(BaseModel):
    startTime: datetime = Field(..., description="Start time of the class")
    duration: float = Field(..., description="Duration of the class")
    finished: bool = Field(..., description="Whether the class is finished")
    rating: int = Field(..., description="Rating of the class")
    comment: str = Field(..., description="Comment of the class")
    isOnline: bool = Field(..., description="Whether the class is online")
    info: Relation = Field(..., description="Info of the class")
