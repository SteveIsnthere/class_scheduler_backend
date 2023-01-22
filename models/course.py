from pydantic import BaseModel, Field


class Course(BaseModel):
    name: str = Field(..., description="Name of the course")
    defaultPrice: int = Field(..., description="Default price of the course")
    defaultDuration: float = Field(..., description="Default duration of the class")
