from bson import ObjectId
from fastapi import HTTPException, status
from database.methods.member import members_collection_name

from database.db import db

plans_collection_name = "plans"


async def post_plan(plan: dict):
    if db.find_one(plans_collection_name, {"startTime": plan["startTime"], "info": plan["info"]}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Plan already exists")
    db.insert(plans_collection_name, plan)
    print(f"Plan {plan['_id']} inserted")
    return {"message": "Plan added"}


async def delete_plan(plan_id: str):
    if not db.find_one(plans_collection_name, {"_id": ObjectId(plan_id)}):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    db.delete_one(plans_collection_name, {"_id": ObjectId(plan_id)})
    print(f"Plan {plan_id} deleted")
    return {"message": "Plan deleted"}


async def update_plan(plan_id: str, new_plan: dict):
    await delete_plan(plan_id)
    await post_plan(new_plan)
    print(f"Plan {plan_id} updated")
    return {"message": "Plan updated"}


async def get_plan_by_member(member_nickname: str):
    member = db.find_one(members_collection_name, {"nickname": member_nickname})
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    member["_id"] = str(member["_id"])
    return list(member["plans"])
