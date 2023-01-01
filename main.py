from database.db import db
from dummy_data import generate_dummy_data
import asyncio
import uvicorn

# asyncio.run(generate_dummy_data(db))
#
if __name__ == "__main__":
    uvicorn.run("server.server:app", reload=True)
