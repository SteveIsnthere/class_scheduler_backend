from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from database.methods.member import *
from models.member import Member

router = APIRouter()


@router.post("/")
async def create_member(new_member: Member = Body(...)):
    new_member = jsonable_encoder(new_member)
    await post_member(new_member)
    return


@router.delete("/{member_nick_name}")
async def remove_member(member_nick_name: str):
    await delete_member(member_nick_name)
    return


@router.get("/all")
async def get_all_of_members():
    result = await get_all_members()
    return result


@router.get("/{member_nick_name}")
async def get_one_member(member_nick_name: str):
    result = await get_member(member_nick_name)
    return result
