# from fastapi import FastAPI
#
# from server.router import router as StudentRouter
#
# app = FastAPI()
#
# app.include_router(StudentRouter, tags=["Student"], prefix="/student")
#
#
# @app.get("/", tags=["Root"])
# async def read_root():
#     return {"message": "Welcome to this fantastic app!"}