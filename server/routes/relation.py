from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from database.methods.relation import *
from models.relation import Relation

router = APIRouter()


@router.post("/")
async def create_relation(new_relation: Relation = Body(...)):
    new_relation = jsonable_encoder(new_relation)
    await post_relation(new_relation)
    return


@router.delete("/{relation_id}")
async def remove_relation(relation_id: str):
    await delete_relation(relation_id)
    return


@router.put("/{relation_id}")
async def update_relation(relation_id: str, new_relation: Relation = Body(...)):
    new_relation = jsonable_encoder(new_relation)
    await replace_relation(relation_id, new_relation)
    return


@router.get("/member/{member_nick_name}")
async def get_relations_of_a_member(member_nick_name: str):
    return await get_relations_by_member(member_nick_name)


@router.get("/all")
async def get_all_of_relations():
    result = await get_all_relations()
    return result
