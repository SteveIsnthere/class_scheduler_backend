from typing import List

from pydantic import BaseModel, Field


class SystemData(BaseModel):
    adminNameList: List[str] = Field(..., description="List of admin names")
    openingTime: int = Field(..., description="Opening time of the school")
    closingTime: int = Field(..., description="Closing time of the school")
