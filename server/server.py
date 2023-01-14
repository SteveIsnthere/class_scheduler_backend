from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from database.auth import auth_user
from server.routes.class_ import router as class_router
from server.routes.course import router as course_router
from server.routes.plan import router as plan_router
from server.routes.member import router as member_router
from server.routes.relation import router as relation_router
from server.routes.message import router as message_router
from server.routes.admin import router as admin_router

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
app.include_router(message_router, prefix="/message")
app.include_router(admin_router, prefix="/admin")


# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     if request.method != "OPTIONS":
#         nickname, password = request.headers.get("nickname"), request.headers.get("password")
#         if not auth_user(nickname, password):
#             # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
#             # return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
#             return JSONResponse(status_code=401, content={"detail": "Invalid username or password"},
#                                 headers={"Access-Control-Allow-Origin": "http://localhost:4200",
#                                          "Access-Control-Allow-Credentials": "true"})
#     return await call_next(request)
#

@app.get("/", tags=["Root"])
async def read_root(request: Request):
    return "You shall pass"
