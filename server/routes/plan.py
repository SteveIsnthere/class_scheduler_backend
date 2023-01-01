from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from database.methods.plan import *
from models.class_plan import ClassPlan

router = APIRouter()


@router.post("/")
async def create_plan(new_plan: ClassPlan = Body(...)):
    new_plan = jsonable_encoder(new_plan)
    await post_plan(new_plan)
    return


@router.delete("/{plan_id}")
async def remove_plan(plan_id: str):
    await delete_plan(plan_id)
    return


@router.put("/{plan_id}")
async def update_plan(plan_id: str, new_plan: ClassPlan = Body(...)):
    new_plan = jsonable_encoder(new_plan)
    await replace_plan(plan_id, new_plan)
    return


@router.get("/member/{member_nick_name}")
async def get_plans_of_a_member(member_nick_name: str):
    return await get_plans_by_member(member_nick_name)
