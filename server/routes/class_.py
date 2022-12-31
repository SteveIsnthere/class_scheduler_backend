from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from database.methods.class_ import post_class, delete_class, replace_class, get_one_week_of_classes, \
    get_one_week_of_classes_of_a_member
from models.class_instance import ClassInstance

router = APIRouter()


@router.post("/")
async def create_class(new_class: ClassInstance = Body(...)):
    new_class = jsonable_encoder(new_class)
    await post_class(new_class)
    return


@router.delete("/{class_id}")
async def remove_class(class_id: str):
    await delete_class(class_id)
    return


@router.put("/{class_id}")
async def update_class(class_id: str, new_class: ClassInstance = Body(...)):
    new_class = jsonable_encoder(new_class)
    await replace_class(class_id, new_class)
    return


@router.get("/oneweek/{offset}")
async def get_classes_in_one_week(offset: int):
    result = await get_one_week_of_classes(offset)
    return result


@router.get("/memberoneweek/{offset}/{member_nick_name}")
async def get_classes_in_one_week_of_a_member(offset: int, member_nick_name: str):
    return await get_one_week_of_classes_of_a_member(offset, member_nick_name)
