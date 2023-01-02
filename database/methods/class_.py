from bson import ObjectId
from fastapi import HTTPException, status
from database.methods.member import members_collection_name
from datetime import datetime, timedelta
from database.db import db

classes_collection_name = "classes"


async def post_class(class_: dict):
    # insert class into database
    # check if class already exists
    if db.find_one(classes_collection_name, {"startTime": class_["startTime"], "info": class_["info"]}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Class already exists")
    db.insert(classes_collection_name, class_)
    print(f"Class {class_} inserted")
    return {"message": "Class added"}


async def delete_class(class_id: str):
    # delete class from database
    # check if class exists
    class_id = ObjectId(class_id)
    if not db.find_one(classes_collection_name, {"_id": class_id}):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class not found")
    db.delete_one(classes_collection_name, {"_id": class_id})
    print(f"Class {class_id} deleted")
    return {"message": "Class deleted"}


async def replace_class(_id: str, class_: dict):
    # update class in database
    # check if class exists
    await delete_class(_id)
    await post_class(class_)
    print(f"Class {class_} updated")
    return {"message": "Class updated"}


def get_dates_in_one_week(week: int):
    # get all dates in a week
    # parameter week is the number of the week offset from the current week
    # e.g. week=0 is the current week, week=1 is the next week, week=-1 is the previous week
    # get the start time of the week
    today = datetime.today()
    start = today + timedelta(days=7 * week - today.weekday())
    start = start.replace(hour=0, minute=0, second=0, microsecond=0)

    # get the end time of the week
    end = start + timedelta(days=7)

    # get all dates in the week
    dates = []
    while start < end:
        dates.append(str(start))
        start += timedelta(days=1)
    return dates


async def get_one_week_of_classes(week: int):
    # get all classes in a week from database
    # parameter week is the number of the week offset from the current week
    # e.g. week=0 is the current week, week=1 is the next week, week=-1 is the previous week

    # get the start time of the week
    today = datetime.today()
    start = today + timedelta(days=7 * week - today.weekday())
    start = start.replace(hour=0, minute=0, second=0, microsecond=0)

    # get the end time of the week
    end = start + timedelta(days=7)

    # get all classes in the week
    classes = list(db.find_many(classes_collection_name, {"startTime": {"$gte": start, "$lt": end}}))
    for c in classes:
        c["_id"] = str(c["_id"])
    return list(classes)


async def get_one_week_of_classes_of_a_member(week: int, member_nick_name: str):
    # get all classes in a week of a member from database
    # parameter week is the number of the week offset from the current week
    # e.g. week=0 is the current week, week=1 is the next week, week=-1 is the previous week
    # get the start time of the week
    today = datetime.today()
    start = today + timedelta(days=7 * week - today.weekday())
    start = start.replace(hour=0, minute=0, second=0, microsecond=0)

    # get the end time of the week
    end = start + timedelta(days=7)

    # check is member teacher or student
    member = db.find_one(members_collection_name, {"nickname": member_nick_name})
    # if member does not exist
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")

    if member["isTeacher"]:
        # get all classes in the week
        classes = list(db.find_many(classes_collection_name,
                                    {"startTime": {"$gte": start, "$lt": end}, "info.teacher": member_nick_name}))
        for c in classes:
            c["_id"] = str(c["_id"])
        return classes
    else:
        # get all classes in the week
        classes = list(db.find_many(classes_collection_name,
                                    {"startTime": {"$gte": start, "$lt": end}, "info.student": member_nick_name}))
        for c in classes:
            c["_id"] = str(c["_id"])
        return classes
