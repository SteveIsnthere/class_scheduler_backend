import json

import pymongo

connection_string = "mongodb://localhost:27017/"
db_name = "class_scheduler"


def to_dict(obj):
    # return json.loads(json.dumps(obj, default=lambda o: o.__dict__))
    # return obj.__dict__
    if not hasattr(obj, "__dict__"):
        return obj
    result = {}
    for key, val in obj.__dict__.items():
        if key.startswith("_"):
            continue
        element = []
        if isinstance(val, list):
            for item in val:
                element.append(to_dict(item))
        else:
            element = to_dict(val)
        result[key] = element
    return result


class DataBase:
    def __init__(self):
        self.db = pymongo.MongoClient(connection_string)[db_name]

    def get_collections(self):
        return self.db.list_collection_names()

    def insert(self, collection, data):
        # insert recursively if is a list, otherwise insert directly
        if isinstance(data, list):
            dicts = []
            for item in data:
                dicts.append(to_dict(item))
            self.db[collection].insert_many(dicts)
        else:
            self.db[collection].insert_one(to_dict(data))

    def find_one(self, collection, query):
        return self.db[collection].find_one(query)

    def find_many(self, collection, query):
        return self.db[collection].find(query)

    def update(self, collection, query, data):
        self.db[collection].update_one(query, data)

    def delete_one(self, collection, query):
        self.db[collection].delete_one(query)

    def delete_many(self, collection, query):
        self.db[collection].delete_many(query)


db = DataBase()

