from fastapi import FastAPI

from server.routes.class_ import router as class_router

app = FastAPI()

app.include_router(class_router, prefix="/class")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
