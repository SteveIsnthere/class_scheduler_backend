from datetime import datetime

import pymongo
from bson import ObjectId
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from database.db import db, obj_id_to_str

router = APIRouter()


@router.post("/")
async def post_message(new_message=Body(...)):
    new_message = jsonable_encoder(new_message)
    new_message['_id'] = ObjectId()
    new_message["time"] = datetime.now()
    db.insert('messages', new_message)
    print(new_message)
    return


@router.get("/{nickname}")
async def get_messages(nickname: str):
    result = obj_id_to_str(
        list(db.find_many('messages', {'receiverNickName': nickname}).sort('time', pymongo.DESCENDING)))
    return result


@router.delete("/{_id}")
async def delete_message(_id: str):
    db.delete_one('messages', {'_id': ObjectId(_id)})
    return
