from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from database.methods.course import post_course, get_members_by_course, get_teachers_by_course, get_students_by_course, \
    get_all_courses, find_course_by_name
from models.course import Course

router = APIRouter()


@router.post("/")
async def create_course(new_course: Course = Body(...)):
    new_course = jsonable_encoder(new_course)
    await post_course(new_course)
    return


@router.get("/teachers/{course_name}")
async def get_teachers(course_name: str):
    result = await get_teachers_by_course(course_name)
    return result


@router.get("/students/{course_name}")
async def get_students(course_name: str):
    result = await get_students_by_course(course_name)
    return result


@router.get("/all")
async def get_all_of_courses():
    result = await get_all_courses()
    return result


@router.get("/{course_name}")
async def get_course(course_name: str):
    result = await find_course_by_name(course_name)
    return result
