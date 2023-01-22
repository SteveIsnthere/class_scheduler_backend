from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from database.db import db, obj_id_to_str

router = APIRouter()


@router.get("/marked_members/{nickname}")
async def add_marked_member(nickname: str):
    mark_record = {"nickname": nickname}
    if db.find_one('marked_members', mark_record):
        # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Class already exists")
        return {"message": "member already marked"}
    db.insert('marked_members', jsonable_encoder(mark_record))
    print("marked member" + nickname)
    return {"marked member" + nickname}


@router.get("/marked_members")
async def get_marked_members():
    result = obj_id_to_str(list(db.find_many('marked_members', {})))
    members: [str] = []
    for record in result:
        members.append(record['nickname'])
    return members


@router.delete("/marked_members/{nickname}")
async def delete_marked_member(nickname: str):
    mark_record = {"nickname": nickname}
    db.delete_one('marked_members', mark_record)
    return {"marked member" + nickname + "deleted"}
