from database.db import db


def auth_user(username: str, password: str):
    user = db.find_one("members", {"nickname": username, "password": password})
    print(username,password)
    if user is None:
        return False
    return True