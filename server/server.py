from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from database.auth import auth_user
from server.routes.class_ import router as class_router
from server.routes.course import router as course_router
from server.routes.plan import router as plan_router
from server.routes.member import router as member_router
from server.routes.relation import router as relation_router

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=[
                       "http://localhost:4200",
                   ],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"], )

app.include_router(class_router, prefix="/class")
app.include_router(course_router, prefix="/course")
app.include_router(plan_router, prefix="/plan")
app.include_router(member_router, prefix="/member")
app.include_router(relation_router, prefix="/relation")


# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     nickname, password = request.cookies.get("nickname"), request.cookies.get("password")
#     print(nickname, password)
#     if not auth_user(nickname, password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
#     return await call_next(request)


@app.get("/", tags=["Root"])
async def read_root(request: Request):
    nickname, password = request.cookies.get("nickname"), request.cookies.get("password")
    print(nickname, password)
    return "You shall pass"
