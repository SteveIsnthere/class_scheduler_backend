from bson import ObjectId
from fastapi import HTTPException, status

from database.methods.course import get_all_courses, post_course, find_course_by_name
from database.methods.member import members_collection_name, get_member, replace_member
from database.db import db, to_dict
from models.course import Course
from models.relation import Relation

relation_collection_name = "relations"


async def post_relation(relation: dict):
    # insert relation into database
    # check if relation already exists
    if db.find_one(relation_collection_name, {"courseName": relation["courseName"], "teacher": relation["teacher"],
                                              "student": relation["student"]}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Relation already exists")
    teacher = await get_member(relation["teacher"])
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    student = await get_member(relation["student"])
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    new_course = Course(
        name=relation["courseName"],
        defaultPrice=relation["price"],
        defaultDuration=2
    )
    find_result = await find_course_by_name(relation["courseName"])
    if find_result is None:
        await post_course(to_dict(new_course))
    else:
        new_course = find_result

    teacher["relations"].append(relation)
    if new_course not in teacher["courses"]:
        teacher["courses"].append(new_course)
    await replace_member(teacher["nickname"], teacher)

    student["relations"].append(relation)
    if new_course not in student["courses"]:
        student["courses"].append(new_course)
    await replace_member(student["nickname"], student)

    db.insert(relation_collection_name, relation)
    print(f"Relation {relation['_id']} inserted")
    return {"message": "Relation added"}


async def delete_relation(relation_id: str):
    # delete relation from database
    # check if relation exists
    relation = db.find_one(relation_collection_name, {"_id": ObjectId(relation_id)})
    if not relation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relation not found")
    teacher = await get_member(relation["teacher"])
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    student = await get_member(relation["student"])
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    relation = Relation(**relation)
    teacher["relations"].remove(relation)
    student["relations"].remove(relation)
    await replace_member(teacher["nickname"], teacher)
    await replace_member(student["nickname"], student)
    db.delete_one(relation_collection_name, {"_id": ObjectId(relation_id)})

    print(f"Relation {relation_id} deleted")
    return {"message": "Relation deleted"}


async def replace_relation(relation_id: str, new_relation: dict):
    # update relation in database
    relation = db.find_one(relation_collection_name, {"_id": ObjectId(relation_id)})
    if not relation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relation not found")
    db.delete_one(relation_collection_name, {"_id": ObjectId(relation_id)})
    await post_relation(new_relation)
    print(f"Relation {relation_id} updated  (not inserted)")
    return {"message": "Relation updated"}


async def get_relations_by_member(member_nickname: str):
    # get relation from database
    # check if relation exists
    # check is member is a teacher or a student
    member = db.find_one(members_collection_name, {"nickname": member_nickname})
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")

    if member["isTeacher"]:
        relations = list(db.find_many(relation_collection_name, {"teacher": member_nickname}))
        for c in relations:
            c["_id"] = str(c["_id"])
        return relations
    else:
        relations = list(db.find_many(relation_collection_name, {"student": member_nickname}))
        for c in relations:
            c["_id"] = str(c["_id"])
        return relations


async def get_all_relations():
    # get all relations from database
    relations = list(db.find_many(relation_collection_name, {}))
    for c in relations:
        c["_id"] = str(c["_id"])
    return relations
