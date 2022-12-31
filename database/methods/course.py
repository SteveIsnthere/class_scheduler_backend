from bson import ObjectId
from fastapi import HTTPException, status
from database.methods.member import members_collection_name
from database.db import db

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
    # get teachers of a course from database
    # check if course exists
    course = db.find_one(courses_collection_name, {"name": course_name})
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    teachers = list(db.find_many(members_collection_name, {"relations": {"$elemMatch": {"courseName": course_name}}}))
    for c in teachers:
        c["_id"] = str(c["_id"])
    return teachers


async def get_teachers_by_course(course_name: str):
    # get teachers of a course from database
    # check if course exists
    members = await get_members_by_course(course_name)
    teachers = list([m for m in members if m["isTeacher"]])
    for c in teachers:
        c["_id"] = str(c["_id"])
    return teachers


async def get_students_by_course(course_name: str):
    # get students of a course from database
    # check if course exists
    members = await get_members_by_course(course_name)
    students = list([m for m in members if not m["isTeacher"]])
    for c in students:
        c["_id"] = str(c["_id"])
    return students


async def get_all_courses():
    # get all courses from database
    courses = list(db.find_many(courses_collection_name, {}))
    for c in courses:
        c["_id"] = str(c["_id"])
    return courses


async def find_course_by_name(course_name: str):
    # find course by name
    course = db.find_one(courses_collection_name, {"name": course_name})
    course["_id"] = str(course["_id"])
    return course
