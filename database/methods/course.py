from fastapi import HTTPException, status

from database.db import db, obj_id_to_str
from database.methods.member import members_collection_name

courses_collection_name = "courses"


async def post_course(course: dict):
    # insert course into database
    # check if course already exists
    if db.find_one(courses_collection_name, {"name": course["name"]}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course already exists")
    db.insert(courses_collection_name, course)
    print(f"Course {course['_id']} inserted")
    return {"message": "Course added"}


async def get_members_by_course(course_name: str):
    # get members of a course from database
    # check if course exists
    members = list(db.find_many(members_collection_name, {"courses.name": course_name}))
    return obj_id_to_str(members)


async def get_teachers_by_course(course_name: str):
    # get teachers of a course from database
    # check if course exists
    members = await get_members_by_course(course_name)
    teachers = list([m for m in members if m["isTeacher"]])
    return teachers


async def get_students_by_course(course_name: str):
    # get students of a course from database
    # check if course exists
    members = await get_members_by_course(course_name)
    students = list([m for m in members if not m["isTeacher"]])
    return students


async def get_all_courses():
    # get all courses from database
    courses = list(db.find_many(courses_collection_name, {}))
    return obj_id_to_str(courses)


async def find_course_by_name(course_name: str):
    # find course by name
    course = db.find_one(courses_collection_name, {"name": course_name})
    course["_id"] = str(course["_id"])
    return course
