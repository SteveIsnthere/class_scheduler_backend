from pydantic import BaseModel, EmailStr, Field
from typing import List

from models.class_plan import ClassPlan
from models.course import Course
from models.relation import Relation
from models.unable_time import UnableTime


class Member (BaseModel):
    name: str = Field(..., description="Name of the member")
    nickname: str = Field(..., description="Unique nickname of the member")
    email: EmailStr = Field(..., description="Email of the member")
    phone: str = Field(..., description="Phone number of the member")
    password: str = Field(..., description="Password of the member")
    isTeacher: bool = Field(..., description="Whether the member is a teacher")
    about: str = Field(..., description="About the member")
    noteToAdmin: str = Field(..., description="Note to admin")
    courses: List[Course] = Field(..., description="Courses taken by the member")
    relations: List[Relation] = Field(..., description="Relations of the member")
    plans: List[ClassPlan] = Field(..., description="Plans of the member")
    unableTimes: List[UnableTime] = Field(..., description="Unable times of the member")
