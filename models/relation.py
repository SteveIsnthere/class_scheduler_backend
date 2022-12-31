from pydantic import BaseModel, Field


class Relation(BaseModel):
    courseName: str = Field(..., description="Name of the course")
    price: int = Field(..., description="Price of the class")
    teacher: str = Field(..., description="Teacher of the class")
    student: str = Field(..., description="Student of the class")
    classPerWeek: int = Field(..., description="Class per week of the class")
