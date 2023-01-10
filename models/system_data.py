from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class SystemData(BaseModel):
    adminNameList: List[str] = Field(..., description="List of admin names")
    openingTime: int = Field(..., description="Opening time of the school")
    closingTime: int = Field(..., description="Closing time of the school")
