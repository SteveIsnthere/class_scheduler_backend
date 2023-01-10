from bson import ObjectId
from fastapi import HTTPException, status

from database.db import db

members_collection_name = "members"


async def post_member(member: dict):
    # insert member into database
    # check if member already exists
    if db.find_one(members_collection_name, {"nickname": member["nickname"]}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Member already exists")
    db.insert(members_collection_name, member)
    print(f"Member {member['nickname']} inserted")
    return {"message": "Member added"}


async def delete_member(member_nickname: str):
    # delete member from database
    # check if member exists
    if not db.find_one(members_collection_name, {"nickname": member_nickname}):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")

    # delete member from all relations
    db.delete_many("relations", {"teacher": member_nickname})
    db.delete_many("relations", {"student": member_nickname})

    # delete all plans of member
    db.delete_many("plans", {"info.teacher": member_nickname})
    db.delete_many("plans", {"info.student": member_nickname})

    # delete all classes of member
    db.delete_many("classes", {"info.teacher": member_nickname})
    db.delete_many("classes", {"info.student": member_nickname})

    db.delete_one(members_collection_name, {"nickname": member_nickname})
    print(f"Member {member_nickname} deleted")
    return {"message": "Member deleted"}


async def replace_member(member_nickname: str, new_member: dict):
    # update member in database
    # check if member exists
    if not db.find_one(members_collection_name, {"nickname": member_nickname}):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    new_member.pop('_id', None)
    new_values = {"$set": new_member}
    db.update(members_collection_name, {"nickname": member_nickname}, new_values)
    print(f"Member {member_nickname} updated")
    return {"message": "Member updated"}


async def get_member(member_nickname: str):
    # get member from database
    # check if member exists
    member = db.find_one(members_collection_name, {"nickname": member_nickname})
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    member["_id"] = str(member["_id"])
    # member['password'] = '********'
    return member


async def get_all_members():
    # get all members from database
    members = list(db.find_many(members_collection_name, {}))
    for c in members:
        c["_id"] = str(c["_id"])
        # c['password'] = '********'
    return members
