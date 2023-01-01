from fastapi import FastAPI, Request
from server.routes.class_ import router as class_router
from server.routes.course import router as course_router
from server.routes.plan import router as plan_router
from server.routes.member import router as member_router
from server.routes.relation import router as relation_router

app = FastAPI()

app.include_router(class_router, prefix="/class")
app.include_router(course_router, prefix="/course")
app.include_router(plan_router, prefix="/plan")
app.include_router(member_router, prefix="/member")
app.include_router(relation_router, prefix="/relation")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
