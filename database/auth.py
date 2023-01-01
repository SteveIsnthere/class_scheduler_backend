from database.db import db
from fastapi import HTTPException, status


def auth_user(username: str, password: str):
    user = db.find_one("users", {"nickname": username, "password": password})
    if not user:
        return False
    return True

